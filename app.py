from flask import Flask, request, redirect, render_template, jsonify, session
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm

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

@app.route("/register", methods=["GET", "POST"])
def register():
    """Show register form so that new users can sign up"""

    if "username" in session:
        return redirect(f"users/{session['username']}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)

        db.session.commit()
        session["username"] = user.username

        return redirect(f"users/{user.username}")

    else:
        return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Show form for user to login"""

    if "username" in session:
        return redirect(f"users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect(f"users/{user.username}")
        else:
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    """Logout user from site"""

    session.pop("username")

    return redirect("/login")

@app.route("/users/<username>")
def show_user(username):
    """Show page for logged in user"""

    if "username" not in session or username != session['username']:
        return redirect("/login")

    user = User.query.get(username)
    form = DeleteForm()

    return render_template("show.html", user=user, form=form)

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Delete user"""

    if "username" not in session or username != session['username']:
        return redirect("/login")

    user = User.query.get(username)

    db.session.delete(user)
    db.session.commit()

    session.pop("username")

    return redirect("/login")



@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """Create new feedback"""

    if "username" not in session or username != session['username']:
        return render_template("/register")

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title = title,
            content = content,
            username = username
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("add_feedback.html", form=form)

@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Edit feedback"""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        return render_template("/register")

    form = FeedbackForm()

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("edit_feedback.html", form=form, feedback=feedback)

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback"""

    feedback = Feedback.query.get(feedback_id)
        
    if "username" not in session or feedback.username != session['username']:
        return render_template("/register")

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")

