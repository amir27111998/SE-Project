from flask_wtf import Form
from wtforms import SubmitField
from flask_wtf.file import FileField,FileAllowed,FileRequired
from flask_uploads import UploadSet


filesAllowed=UploadSet('video',extensions=("mp4","avi"))

class Analyze(Form):
    Video=FileField("Video",validators=[FileRequired("You must upload a video before analysis"),
                                        FileAllowed(filesAllowed,message="You must upload a valid video")])
    submit=SubmitField("Analyze")