from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.validators import *

MAX_TITLE_LENGTH = 50
MAX_EMAIL_LENGTH = 100
MAX_USERNAME_LENGTH = 100
MAX_POST_CONTENT_LENGTH = 1000
MAX_COMMENT_CONTENT_LENGTH = 200

class RegisterLoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=MAX_USERNAME_LENGTH)])
    email = EmailField("Email Address", validators=[Email(), Length(max=MAX_EMAIL_LENGTH)])
    password = PasswordField("Password", validators=[DataRequired()])
    confirmPassword = PasswordField("Confirm Password")

class PostForm(FlaskForm):
    title = StringField("Comment", validators=[DataRequired(), Length(max=MAX_TITLE_LENGTH)])
    content = StringField("Comment", validators=[Length(max=MAX_POST_CONTENT_LENGTH)])

class CommentForm(FlaskForm):
    content = StringField("Comment", validators=[DataRequired(), Length(max=MAX_COMMENT_CONTENT_LENGTH)])