#peoples
#User Profile
#dahboard
#User list
#Analyzer
#Add Users

from flask import Blueprint,render_template,request
from project.controllers.admin import login_required
from project.controllers.analyzer import create_path,deleteVideos,captureFrames,deleteFramesFaces
import os,time
import numpy as np

panel=Blueprint('dashboard',__name__,url_prefix='/dashboard',static_folder='../static',static_url_path="/static")

@panel.route('/')
@login_required
def index():
    return render_template('dashboard.html')

@panel.route('/peoples')
@login_required
def peoples():
    return render_template('tables.html')

@panel.route('/profile')
@login_required
def profile():
    return render_template("profile.html")

@panel.route('/create')
@login_required
def create():
    return render_template("user_registration.html")

@panel.route('/analyzer',methods=["GET","POST"])
@login_required
def analyze():
    deleteVideos()
    deleteFramesFaces()
    if request.method=="POST":
        res=int(time.time())
        videoData=request.files['image']
        path=create_path(res)
        videoData.save(path)
        return str(res)
    return render_template("analyze.html")

@panel.route('/capture',methods=["GET"])
@login_required
def capture():
    if request.method=="GET":
        video=request.args.get("name")
        return captureFrames(video)