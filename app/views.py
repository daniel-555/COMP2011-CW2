from flask import redirect, render_template, request
from flask_login import current_user
from app import app, db, admin
from flask_admin.contrib.sqla import ModelView
from .models import User, Post, Comment, Like
from .forms import CommentForm, PostForm
import json

# Temporary for development, remove for final build
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Comment, db.session))
admin.add_view(ModelView(Like, db.session))

# Test post data to check that posts render as they should
# Will be replaced with database entries after the query is implemented


@app.route("/", methods=['GET'])
def home():
    # Show the login page if logged out
    # if logged in show all posts in a feed ordered newestFirst/mostLiked/etc...

    posts = []

    if current_user.is_authenticated:
        posts = db.session.execute(db.select(Post).order_by(Post.created_at))
        posts = [post[0] for post in posts]

    return render_template("home.html", title="Home", posts=posts)

@app.route("/user/<string:username>", methods=['GET', 'POST'])
@app.route("/user", methods=['GET', 'POST'])
def userPage(username=None):
    # Show a user's profile page if logged in
    # redirect to login page if logged out
    if not current_user.is_authenticated:
        return redirect("/")
    
    # if no username is provided then show the currently logged in user's page
    if username:
        user = db.session.execute(db.select(User).filter_by(username=username)).scalar()
    else:
        user = db.session.execute(db.select(User).filter_by(id=current_user.get_id())).scalar()
        username = user.username


    if not user:
        return redirect("/")
 
    likes_received = sum([len(post.likes) for post in user.posts])

    return render_template("userProfilePage.html", title=f"{username}", posts=user.posts, likes_received=likes_received)

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
@app.route("/view-post", methods=['GET', 'POST'])
def viewPost(post_id=None):
    # view a specific post from a user in order to comment on it
    # redirect to login if logged out
    
    
    if not current_user.is_authenticated or not post_id:
        return redirect("/")
    
    post = db.session.execute(db.select(Post).filter_by(id=post_id)).scalar()

    if not post:
        return redirect("/")
    
    form = CommentForm()

    if form.validate_on_submit():
        comment_creator = current_user.get_id()
        content = form.content.data

        comment = Comment(comment_creator=comment_creator, post_id=post_id, content=content)
        db.session.add(comment)
        db.session.commit()

        return redirect(f"/view-post/{post_id}")

    return render_template("viewPost.html", title=f"viewing post {post_id}", post=post, form=form)

@app.route("/like-post", methods=['POST'])
def likePost():
    # check if the user has already liked the post
    # if not then create a new like table entry
    # return the updated like count

    data = json.loads(request.data)
    post_id = data.get('post_id')
    user_id = current_user.get_id()

    user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar()
    post = db.session.execute(db.select(Post).filter_by(id=post_id)).scalar()

    if not user or not post:
        return json.dumps({'status': '400', 'response': "user or post does not exist"})
    
    for like in user.likes:
        if like in post.likes:
            # Post is already liked by the user
            return json.dumps({'status': 'liked already', 'message': 'Post has already been liked by the user', 'like_count': len(post.likes)})
    
    # Post hasn't been liked yet
    like = Like(user_id=user_id, post_id=post_id)
    db.session.add(like)
    db.session.commit()

    return json.dumps({'status': 200, 'message': 'Post added to user\'s likes', 'like_count': len(post.likes)})

    

