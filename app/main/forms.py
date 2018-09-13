from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Required

class CommentForm(FlaskForm):

 title = StringField('Comment title',validators=[Required()])

 comment = TextAreaField('Comment title')

 submit = SubmitField('Submit')
class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')
class AddPitch(FlaskForm):
    pitch = TextAreaField('Write your pitch',validators =[Required()])
    submit = SubmitField('Submit')
