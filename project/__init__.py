from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app=Flask(__name__)
app.config["SECRET_KEY"]="amir123"
app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:@127.0.0.1/project"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)
Migrate(app,db)
from project.models import User,Role
from project.routes.admin import admin
from project.routes.dashboard import panel

app.register_blueprint(panel)
app.register_blueprint(admin)