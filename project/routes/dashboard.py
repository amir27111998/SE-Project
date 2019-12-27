#peoples
#User Profile
#dahboard
#User list
#Analyzer
#Add Users

from flask import Blueprint,render_template,session
from project.controllers.admin import login_required
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