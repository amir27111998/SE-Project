from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TimeField
from wtforms.validators import DataRequired

class Login(FlaskForm):
    email=StringField("Email",validators=[DataRequired(message="Provide the valid email")])
    password=PasswordField("Password",validators=[DataRequired(message="Password can't be empty")])
    submit=SubmitField("Sign in")