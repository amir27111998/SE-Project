from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TimeField
from wtforms.validators import DataRequired
from project.controllers.admin import get_hash_password
from flask_wtf.file import FileField,FileAllowed
class createUserForm(FlaskForm):
	address = StringField("address",validators=[DataRequired(message="Provide the valid address")])
	email=StringField("Email",validators=[DataRequired(message="Provide the valid email")])
	created_at = StringField(render_kw={'readonly':True})
	username = StringField("username",validators=[DataRequired(message="Provide the valid username")]) 
	password=PasswordField("Password",validators=[DataRequired(message="Password can't be empty")])
	phone=StringField("phoneNo",validators=[DataRequired(message="Provide the valid phoneNo")])
	picture = FileField("Update Profile Picture",validators=[FileAllowed(['jpg','png'])])
	submit=SubmitField("Update Account")
