import os,time
import cv2
from flask import json
import numpy as np
from PIL import Image
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
    listImg={}
    while video.isOpened():
        ret,frame=video.read()
        if frame is None:
            break
        else:
            if counter==0:
                ff=fr.face_locations(frame)
                if ff != []:
                    name="{}.jpg".format(img)
                    fullpath = path+name
                    for rec in ff:
                        top, right, bottom, left=rec
                        cv2.imwrite(facespath+"{}.jpg".format(faces), frame[top-5:bottom+5,left:right])
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                        faces+=1
                    cv2.imwrite(fullpath,frame)
                    listImg[img]=name
                    img+=1
                counter=10
            counter-=1
    video.release()
    return json.dumps(listImg)
