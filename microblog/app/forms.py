# registration class form
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Length

class LoginForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
# The optional validators argument that you see in some of the fields is used to attach validation behaviors to fields.
# The DataRequired validator simply checks that the field is not submitted empty.


class PostsForm(FlaskForm):
    body = TextAreaField('Body', validators=[InputRequired()])
    submit = SubmitField('Post')

class EditDeleteForm(FlaskForm):
    body = TextAreaField('Body', validators=[InputRequired()])
    edit = SubmitField('Edit')
    delete = SubmitField('Delete')