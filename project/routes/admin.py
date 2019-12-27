from flask import Blueprint,render_template,redirect,session,flash
from project.forms.login import Login
from project.controllers.admin import loginLogic,logoutLogic,get_hash_password

admin=Blueprint("admin",__name__)
#######Login#######
@admin.route('/',methods=["GET"])
def index():
    if session.get("USER"):
         return redirect('/dashboard')
    form = Login()
    return render_template("login.html", form=form)

@admin.route('/',methods=['POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        if loginLogic(email,password):
            return redirect('/dashboard')
        else:
            flash("Email or Password does not match")
            return redirect('/')
    else:
        flash(form.errors)
        return redirect('/')



@admin.route('/logout')
def logout():
    logoutLogic()
    return redirect('/')
