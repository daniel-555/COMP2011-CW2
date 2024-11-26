from flask import request
from flask_login import login_required
from app import app, db, login_manager
from .models import User

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)

@app.route("/auth/register", methods=['POST'])
def register():
    
    if request.method == "POST":
        pass
    pass

@app.route("/auth/login", methods=['POST'])
def login():

    if request.method == "POST":
        pass
    pass

@app.route("/auth/logout", methods=['GET', 'POST'])
@login_required
def logout():
    pass
