from flask import redirect, render_template
from flask_login import current_user
from app import app, db, admin
from flask_admin.contrib.sqla import ModelView
from .models import User, Post, Comment, Like
from .forms import PostForm

# Temporary for development, remove for final build
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Comment, db.session))
admin.add_view(ModelView(Like, db.session))


@app.route("/", methods=['GET'])
def home():
    # Show the login page if logged out
    # if logged in show all posts in a feed ordered newestFirst/mostLiked/etc...
    return render_template("home.html", title="Home")

@app.route("/user/<int:userId>", methods=['GET', 'POST'])
def profile(userId=None):
    # Show a user's profile page if logged in
    # redirect to login page if logged out
        
    return render_template("base.html", title="User Profile Page")

@app.route("/create-post", methods=['GET', 'POST'])
def createPost():
    # form to create a post if logged in
    # redirect to login page if logged out
    if not current_user.is_authenticated:
        return redirect("/")

    form = PostForm()

    if form.validate_on_submit():
        post_author = current_user.get_id()
        title = form.title.data
        content = form.content.data

        new_post = Post(post_author=post_author, title=title, content=content)

        db.session.add(new_post)
        db.session.commit()

        return redirect(f"/user/{post_author}")

    return render_template("createPost.html", title="Create a Post", form=form)

@app.route("/view-post/<int:postId>", methods=['GET', 'POST'])
def viewPost(postId=None):
    # view a specific post from a user in order to comment on it
    # redirect to login if logged out
    pass