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


@app.route("/", methods=['GET'])
def home():
    # Show the login page if logged out
    # if logged in show all posts in a feed ordered newestFirst/mostLiked/etc...

    data = []

    if current_user.is_authenticated:
        posts = db.session.execute(db.select(Post).order_by(Post.created_at))
        posts = [post[0] for post in posts]

        for post in posts:
            likes = len(post.likes)
            username = db.session.execute(db.select(User.username).filter_by(id=post.post_author)).scalar()
            data.append((post, username, likes))


    return render_template("home.html", title="Home", post_data=data)

@app.route("/user/<string:username>", methods=['GET', 'POST'])
@app.route("/user", methods=['GET', 'POST'])
def profile(username=None):
    # Show a user's profile page if logged in
    # redirect to login page if logged out
    if not current_user.is_authenticated or not username:
        return redirect("/")
    
    user = db.session.execute(db.select(User).filter_by(username=username)).scalar()

    if not user:
        return redirect("/")
    
    posts = user.posts
    data = []
    for post in posts:
        likes = len(post.likes)
        data.append((post, username, likes))



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
@app.route("/view-post", methods=['GET', 'POST'])
def viewPost(post_id=None):
    # view a specific post from a user in order to comment on it
    # redirect to login if logged out
    
    if not current_user.is_authenticated or not post_id:
        return redirect("/")
    
    # data = {'title': 'This is the post title', 'content': 'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Esse expedita consectetur corrupti a, impedit veniam delectus quas perspiciatis atque aliquam quo commodi laudantium magnam libero, iusto incidunt, labore voluptas! Architecto omnis, ipsum vel nisi facere esse saepe explicabo cumque, iste illum aliquam tempore corrupti asperiores? Quaerat natus, tempora pariatur repudiandae repellat omnis cumque, architecto expedita animi totam dolore consequuntur dolores qui, nobis similique mollitia in reiciendis ducimus beatae perspiciatis voluptatibus alias laborum est ea. Repellendus, necessitatibus? Placeat eum dolorem maiores, delectus ipsam eaque rem unde perferendis aut explicabo praesentium. Quam at excepturi quo, animi ipsam autem iusto atque expedita aliquid.'}

    post = db.session.execute(db.select(Post).filter_by(id=post_id)).scalar()
    likes = len(post.likes)

    data = {
        'post': post,
        'likes': likes 
    }

    return render_template("viewPost.html", title=f"viewing post {post_id}", data=data)