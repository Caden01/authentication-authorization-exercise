from flask import Flask, request, redirect, render_template, jsonify, session
from models import db, connect_db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///auth-exercise"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "alkju88jlkw388"

connect_db(app)
with app.app_context():
    db.create_all()


@app.route("/")
def root():
    """Redirect to register page"""
    

    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Show register form so that new users can sign up"""

    form = RegisterForm()

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

@app.route("/login", methods=["GET", "POST"])
def login():
    """Show form for user to login"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        session["username"] = username.username

        return redirect("/secret")

    else:
        return render_template("login.html", form=form)

@app.route("/secret")
def secret():
    """Secret page for registered users"""

    return render_template("secret.html")