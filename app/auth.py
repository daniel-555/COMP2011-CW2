from flask import render_template, flash, redirect
from flask_login import login_required, login_user
from app import app, db, login_manager
from .models import User
from .forms import LoginForm, RegisterForm

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        print("Form validated successfully")
        
        username = form.username.data
        email = form.email.data
        password = form.password.data

        new_user = User(username=username, email=email, password=password)

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)




    elif form.errors:
        flash(list(form.errors.values())[0][0])
        print(form.errors)

    return render_template("loginPage.html", title="Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Log the user in
        pass

    return render_template("loginPage.html", title="Login", form=form)

@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    pass
