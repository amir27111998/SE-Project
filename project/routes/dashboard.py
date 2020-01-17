#peoples
#User Profile ali karraha hai
#dahboard
#User list
#Analyzer hogya
#Add Users ali karraha hai

from flask import Blueprint,render_template,request,json,session,abort,flash
from project.controllers.admin import login_required
from project.controllers.analyzer import create_path,deleteVideos,captureFrames,deleteFramesFaces,compareFaces,unknownFaces
import time,os,pdfkit
from project.forms.updateAccount import updateAccountForm
from project.controllers.dashboard import gettingTheUseage,getALLUsers,getOneDayTraffic,gettingSystemGrowth
from project.models import Peoples,Links,PeopleLinks,User
from project.controllers.admin import get_hash_password

from project import db

panel=Blueprint('dashboard',__name__,url_prefix='/dashboard',static_folder='../static',static_url_path="/static")

###Mini Controller
def userData():
    return json.loads(session.get("USER"))

def listingLinks(peoples):
    p={};links=[]
    for k in peoples:
        p=k[0]
        links.append([k[2],k[3]])
    return (p,links)
##End
def pathForImage(email):

    path=os.path.abspath("project/static/images/profile_pics/")
    fullpath=os.path.join(path,str(email)+".jpg")
    return fullpath
@panel.route('/')
@login_required
def index():
    user=userData()
    traffic=getOneDayTraffic()
    users = getALLUsers(user["id"])
    return render_template('dashboard.html',user=user,usersList=users,traffic=traffic)

@panel.route('/peoples',methods={'GET'})
@login_required
def peoples():
    user = userData()
    try:
        id=request.args.get('id')
        if not id:
            peoples = Peoples.query.all()
            return render_template('peoples.html', user=user, peoples=peoples)
        elif len(Peoples.query.filter(Peoples.id==id).all()) < 1:
            abort(404)
        people = db.session.query(Peoples,PeopleLinks).join(PeopleLinks,Peoples.id==PeopleLinks.c.peoplesId).filter(Peoples.id==id).all()
        p, links = listingLinks(people)
        if p=={}:
            p=Peoples.query.filter_by(id=id).first()
        return render_template("peopledetail.html", user=user,people=p, links=links)
    except:abort(404)



@panel.route('/profile',methods={'GET','POST'})
@login_required
def profile():
    form = updateAccountForm()
    user = userData()
    
    if form.validate_on_submit():
        if form.picture.data:
        
          #  deleteImage(session['email'])
            path = pathForImage(form.email.data)
            image_file = form.picture.data
            image_file.save(path)
        anotherUser =  User.query.filter_by(email=form.email.data).first()
        if anotherUser:
            flash("Email has already been taken")
            

        else:  

            users = User.query.filter_by(id=user['id']).first()
            users.name = form.username.data
            users.password =get_hash_password(form.password.data)
            users.email = form.email.data
            users. phone = form.phoneNo.data
            
            users.address = form.address.data
            db.session.commit()

            
    

    elif request.method == 'GET':
        form.username.data = user['name']
        form.email.data = user['email']
        form.password.data = user['password']
        form.designation.data = str(user)
        form.phoneNo.data = user['phone']
        form.address.data = user['address']    

    # fullpath=os.path.join("project/static/images/profile_pics/alisyedamir2018@gmail.com.jpg",str(session['email'])+".jpg")
    image_file = "static/images/profile_pics/"+str(user['email'])+".jpg"
    return render_template("profile.html",form = form,image_file=image_file,user = user)
   

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