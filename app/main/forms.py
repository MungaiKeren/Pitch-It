from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,SubmitField,TextAreaField
from wtforms.validators import Required,Email,EqualTo
from wtforms import ValidationError

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Edit bio',validators=[Required()])
    submit = SubmitField('submit')

class PitchNow(FlaskForm):
    title = StringField('Pitch title/category',validators=[Required()])
    pitch = TextAreaField('Pitch my idea',validators=[Required()])
    submit = SubmitField('submit')

class MyComment(FlaskForm):
    comment = TextAreaField('Your comment',validators=[Required()])
    submit = SubmitField('submit')