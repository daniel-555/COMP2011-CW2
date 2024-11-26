from flask import render_template
from app import app, db, admin
from flask_admin.contrib.sqla import ModelView
from .models import User, Post, Comment, Like

# Temporary for development, remove for final build
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Comment, db.session))
admin.add_view(ModelView(Like, db.session))


@app.route("/", methods=['GET'])
def home():
    # Show the login page if logged out
    # if logged in show all posts in a feed ordered newestFirst/mostLiked/etc...
    return render_template("base.html", title="Home")

@app.route("/user/<int:userId>", methods=['GET', 'POST'])
def profile(userId=None):
    # Show a user's profile page if logged in
    # redirect to login page if logged out
    pass

@app.route("/create-post", methods=['GET', 'POST'])
def createPost():
    # form to create a post if logged in
    # redirect to login page if logged out
    pass

@app.route("/view-post/<int:postId>", methods=['GET', 'POST'])
def viewPost(postId=None):
    # view a specific post from a user in order to comment on it
    # redirect to login if logged out
    pass

@app.route("/register", methods=['GET', 'POST'])
def registerForm():
    # The page containing the registration form
    pass

@app.route("/login")
def loginForm():
    # The page containing the login form
    return render_template("loginPage.html", title="Login")