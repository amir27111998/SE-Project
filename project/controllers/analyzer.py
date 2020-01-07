import os,time
import cv2,pickle
from flask import json,session
import numpy as np
import face_recognition as fr
from project.models import Peoples,Images,Links,Logs,PeopleLinks
from project import db

def create_path(timesatmp):
    path=os.path.abspath("project/static/videos/")
    fullpath=os.path.join(path,str(timesatmp)+".mp4")
    return fullpath

def deleteVideos():
    timestamp=time.time()
    path = os.path.abspath("project/static/videos")
    for file in os.listdir(path):
        fullpath=os.path.join(path,file)
        check=timestamp-int(file.split('.')[0])
        hour=1*60*60
        if check>=hour:
            os.remove(fullpath)

def deleteFramesFaces():
    frame = os.path.abspath("project/static/images/frames")
    for file in os.listdir(frame):
        fullpath=os.path.join(frame,file)
        os.remove(fullpath)
    faces = os.path.abspath("project/static/images/faces")
    for file in os.listdir(faces):
        fullpath = os.path.join(faces, file)
        os.remove(fullpath)

def captureFrames(filename):
    path = "project/static/images/frames/"
    facespath = "project/static/images/faces/"
    file=filename+".mp4"
    video=cv2.VideoCapture("project/static/videos/"+file)
    id=json.loads(session["USER"])['id']
    db.session.add(Logs(userID=id))
    db.session.commit()
    img=0;counter=0;faces=0
    classifier = cv2.CascadeClassifier("project/haarcascade_frontalface_default.xml")
    fps = int(round(video.get(cv2.CAP_PROP_FPS)))*2
    listImg={}
    while video.isOpened():
        ret,frame=video.read()
        if frame is None:
            break
        else:
            if counter%fps==0:
                gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                ff=classifier.detectMultiScale(gray,1.3,4)
                if ff != ():
                    name="{}.jpg".format(img)
                    fullpath = path+name
                    for x,y,w,h in ff:
                        if faces%3==0:
                            cropped=cv2.resize(frame[y:y+h,x:x+w],(120,120))
                            cv2.imwrite(facespath+"{}.jpg".format(faces),cropped)
                        faces+=1
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.imwrite(fullpath,frame)
                    listImg[img]=name
                    img+=1
            counter+=1
    video.release()
    return json.dumps(listImg)

def compareFaces():
    data={}
    knowns={}
    with open("datasetEncodings.dat","rb") as file:
        data=pickle.load(file)

    ##data
    encodings = []
    names = []
    for (name, encode) in data.items():
        encodings.append(encode)
        names.append(name)
    encodings = np.array(encodings)
    knowns={}
    for faceImage in os.listdir("project/static/images/faces/"):
        image=cv2.imread("project/static/images/faces/"+faceImage)
        if fr.face_encodings(image)!=[]:
            faceEncoding=fr.face_encodings(image)[0]
            temp=fr.compare_faces(encodings,faceEncoding)
            if True in temp:
                index=temp.index(True)
                os.remove("project/static/images/faces/" + faceImage)
                if index not in list(knowns.keys()):
                    people=Peoples.query.filter_by(id=names[index]).all()[0]
                    knowns[index]=[people.id,people.fullname]
    return json.dumps(knowns)

def unknownFaces():
    folder="project/static/images/faces/"
    encoding=[]
    result=[]
    file=""
    for file in os.listdir(folder)[:1]:
        name=cv2.imread(folder+file)
        if fr.face_encodings(name)!=[]:
            check=fr.face_encodings(name)[0]
            encoding.append(check)
    encoding=np.array(encoding)
    if file!="":
        result.append(file)
    for f in os.listdir(folder):
        name = cv2.imread(folder + f)
        if fr.face_encodings(name) != []:
            check = fr.face_encodings(name)
            cond=fr.compare_faces(encoding,check)
            if cond!=[]:
                if False in cond:
                    encoding=[]
                    encoding.append(fr.face_encodings(name)[0])
                    encoding=np.array(encoding)
                    result.append(f)
    return result


def saveEncodings():
    path = 'project/static/images/peoples/'
    data = {}
    peoples=Peoples.query.all()
    for people in peoples:
        img=Images.query.filter_by(peopleID=people.id).all()[0]
        file=cv2.imread(path+img.imageName)
        top,right,bottom,left=fr.face_locations(file)[0]
        face=file[top:bottom,left:right]
        face=cv2.resize(face,(120,120))
        data[people.id]=fr.face_encodings(face)[0]
    with open('datasetEncodings.dat','wb') as f:
        pickle.dump(data,f)
    return 1

# def configureEncodings(fullname,email,description,phone,links={}):
#     peoplesImages=Peoples(fullname=fullname,email=email,description=description,phone=phone)
#     db.session.add(peoplesImages)
#     db.session.commit()
#     images=Images(imageName="{}.jpg".format(peoplesImages.id),peopleID=peoplesImages.id)
#     db.session.add(images)
#     db.session.commit()
#     for (key,value) in links:
#         url=PeopleLinks.insert().values(peoplesId=peoplesImages.id,linksId=key,url=value)
#         db.session.add(url)
#         db.session.commit()