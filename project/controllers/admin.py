from flask import session,redirect,json
import hashlib
from functools import wraps
from project.models import User
def loginLogic(email,password):
    Password=get_hash_password(password)
    user=User.query.filter_by(email=email,password=Password).first()
    if user:
        session["USER"]=str(user)
        return True
    return False

def logoutLogic():
    session.pop('USER',None)

def get_hash_password(password):
    salt='amir123'
    hashPassword=hashlib.md5((password+''+str(len(password))+''+salt).encode())
    return  str(hashPassword.hexdigest())

def login_required(f):      #decorator function
    @wraps(f)
    def wrap(*args,**kwargs):
        if session.get('USER'):
            return f(*args,**kwargs)
        else:
            return redirect('/')

    return wrap