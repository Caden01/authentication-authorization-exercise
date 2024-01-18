from flask import Flask, request, redirect, render_template, jsonify, session
from models import db, connect_db, User
from forms import registerForm

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///auth-exercise"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "alkju88jlkw388"

connect_db(app)


@app.route("/")
def root():
    """Redirect to register page"""
    

    return redirect("/register")

@app.route("/register")
def register():
    """Show register form so that new users can sign up"""

    form = registerForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(username, password, email, first_name, last_name)

        db.session.commit()
        session["username"] = user.username

        return redirect("/secret")

    else:
        return render_template("register.html", form=form)


