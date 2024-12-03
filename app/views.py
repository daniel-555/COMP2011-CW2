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

# Test post data to check that posts render as they should
# Will be replaced with database entries after the query is implemented

def get_posts(user_filter=None):
    post_data = db.session.execute(db.select(Post).order_by(Post.created_at))
    post_data = [post[0] for post in post_data]

    data = []
    for post in post_data:
        username = db.session.execute(db.select(User.username).filter_by(id=post.post_author)).scalar()

        if user_filter and post.post_author == user_filter:
            data.append((post, username))
        elif not user_filter:
            data.append((post, username))
    
    return data


@app.route("/", methods=['GET'])
def home():
    # Show the login page if logged out
    # if logged in show all posts in a feed ordered newestFirst/mostLiked/etc...

    data = []

    if current_user.is_authenticated:
        data = get_posts()


    return render_template("home.html", title="Home", post_data=data)

@app.route("/user/<string:username>", methods=['GET', 'POST'])
@app.route("/user", methods=['GET', 'POST'])
def profile(username=None):
    # Show a user's profile page if logged in
    # redirect to login page if logged out
    if not current_user.is_authenticated or not username:
        return redirect("/")
    
    user_id = db.session.execute(db.select(User.id).filter_by(username=username)).scalar()

    if not user_id:
        return redirect("/")
    
    data = get_posts(user_filter=user_id)


    return render_template("userProfilePage.html", title=f"{username}", post_data=data)

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

        author = db.session.execute(db.select(User).filter_by(id=post_author)).scalar()

        return redirect(f"/user/{author.username}")

    return render_template("createPost.html", title="Create a Post", form=form)

@app.route("/view-post/<int:post_id>", methods=['GET', 'POST'])
def viewPost(post_id=None):
    # view a specific post from a user in order to comment on it
    # redirect to login if logged out
    
    if not current_user.is_authenticated:
        return redirect("/")