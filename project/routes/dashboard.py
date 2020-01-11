#peoples
#User Profile ali karraha hai
#dahboard
#User list
#Analyzer hogya
#Add Users ali karraha hai

from flask import Blueprint,render_template,request,json,session
from project.controllers.admin import login_required
from project.controllers.analyzer import create_path,deleteVideos,captureFrames,deleteFramesFaces,compareFaces,unknownFaces
import time,os,pdfkit
from project.controllers.dashboard import gettingTheUseage,getALLUsers,getOneDayTraffic,gettingSystemGrowth
panel=Blueprint('dashboard',__name__,url_prefix='/dashboard',static_folder='../static',static_url_path="/static")

def userData():
    return json.loads(session.get("USER"))
@panel.route('/')
@login_required
def index():
    user=userData()
    traffic=getOneDayTraffic()
    users = getALLUsers(user["id"])
    return render_template('dashboard.html',user=user,usersList=users,traffic=traffic)

@panel.route('/peoples')
@login_required
def peoples():
    user = userData()
    return render_template('tables.html',user=user)

@panel.route('/profile')
@login_required
def profile():
    user = userData()
    return render_template("profile.html",user=user)

@panel.route('/create')
@login_required
def create():
    user = userData()
    return render_template("user_registration.html",user=user)

#uses as both post and get
@panel.route('/analyzer',methods=["GET","POST"])
@login_required
def analyze():
    user = userData()
    deleteVideos()
    deleteFramesFaces()
    if request.method=="POST":
        res=int(time.time())
        videoData=request.files['image']
        path=create_path(res)
        videoData.save(path)
        return str(res)
    return render_template("analyze.html",user=user)
##Begning API
@panel.route('/capture',methods=["GET"])
@login_required
def capture():
    if request.method=="GET":
        video=request.args.get("name")
        return captureFrames(video)

@panel.route('/compare',methods=['GET'])
@login_required
def compare():
    if request.method=="GET":
        return compareFaces()

@panel.route('/unknown',methods=['GET'])
@login_required
def config():
    ff=unknownFaces()
    return json.dumps({'result':ff})
## END

@panel.route('/pdf',methods=["POST"])
@login_required
def pdf():
        count=len(os.listdir('project/static/images/frames'))
        persons=json.loads(request.form["person"])
        unknowns=len(json.loads(request.form["unknown"])['result'])

        template=render_template('PDF.html',count=count,persons=persons,unknowns=unknowns)
        config = pdfkit.configuration(wkhtmltopdf=bytes("C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe", 'utf8'))

        options = {
            'encoding': 'base64'
        }
        path='project/static/pdfs/report.pdf'
        pdf=pdfkit.from_string(template,path,configuration=config,options=options)
        return "1"

@panel.route('/uses',methods=["GET"])
@login_required
def usageData():
    id = json.loads(session.get("USER"))["id"]
    logs = gettingTheUseage(id)
    return json.dumps(logs)

@panel.route('/expansion',methods=['GET'])
@login_required
def sysExpansion():
    id=json.loads(session.get("USER"))["id"]
    growth=gettingSystemGrowth(id)
    return json.dumps(growth)