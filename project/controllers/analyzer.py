import os,time
import cv2,pickle
from flask import json
import numpy as np
import face_recognition as fr

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
    img=0;counter=10;faces=0
    classifier = cv2.CascadeClassifier("project/haarcascade_frontalface_default.xml")
    listImg={}
    while video.isOpened():
        ret,frame=video.read()
        if frame is None:
            break
        else:
            if counter==0:
                gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                ff=classifier.detectMultiScale(gray,1.3,4)
                if ff != ():
                    name="{}.jpg".format(img)
                    fullpath = path+name
                    for x,y,w,h in ff:
                        if faces%10==0:
                            cropped=cv2.resize(frame[y:y+h,x:x+w],(120,120))
                            cv2.imwrite(facespath+"{}.jpg".format(faces),cropped)
                        faces+=1
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.imwrite(fullpath,frame)
                    listImg[img]=name
                    img+=1
                counter=10
            counter-=1
    video.release()
    return json.dumps(listImg)

def compareFaces():
    data={}
    knowns={}
    with open("project/dataset.dat","rb") as file:
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
                    knowns[index]=names[index]

    return json.dumps(knowns)