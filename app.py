from flask import Flask, request, redirect, render_template, jsonify
from models import db, connect_db, User

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