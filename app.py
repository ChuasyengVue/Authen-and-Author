from flask import Flask, render_template, redirect, flash, session # type: ignore
from flask_debugtoolbar import DebugToolbarExtension # type: ignore

from models import db, connect_db, User, Feedback
from forms import UserForm, LoginForm, FeedbackForm, DeleteForm


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///Authen_Author'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False


connect_db(app)
app.app_context().push()
db.create_all()


app.config['SECRET_KEY'] = 'SecretKey1!'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)


@app.route("/")
def homepage():
    """Homepage, redirect to register"""

    return redirect("/register")


@app.route("/users/<username>")
def show_users_information(username):
    """Shows info on logged in users"""

    if "username" not in session or username != session['username']:
        flash("Please Login First!", "danger")
        return redirect("/login")
    
    user = User.query.get(username)
    
    form = DeleteForm()

    feedback = Feedback.query.all()

    return render_template("users/display.html", user=user, form=form, username=username, feedback=feedback)


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """Register/create a user when submitted"""

    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        new_user = User.register(username, password, first_name,
                                 last_name, email)
        
        db.session.add(new_user)
        db.session.commit()

        session['username'] = new_user.username
        
        flash(f'Welcome! {new_user.username}  You Have Successfully Created Your Account!', "success")
        return redirect(f"/users/{new_user.username}")

    return render_template("users/register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def user_login():
    """Login for existing users"""

    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        existing_user = User.authenticate(username, password)

        if existing_user:
            flash(f"Welcome Back, {existing_user.username}!", "info")
            session['username'] = existing_user.username
            return redirect(f"/users/{existing_user.username}")
        else:
            form.username.errors = ["Invalid username/password."]

    return render_template("users/login.html", form=form)


@app.route("/logout")
def logout_user():
    """Logs out current user"""

    session.pop('username')
    
    flash(f"You have successfully logged out!", "success")
    return redirect('/login')


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Delete the user and all their contents."""

    if "username" not in session or username != session["username"]:
        flash("Please Login First!", "danger")
        return redirect("/login")
    
    user = User.query.get(username)

    db.session.delete(user)
    db.session.commit()

    session.pop("username")

    return redirect("/login")


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """Shows feedback form and allow user to add feedbacks"""

    if "username" not in session or username != session['username']:
        flash("Please Login First!", "danger")
        return redirect("/login")
    
    form = FeedbackForm()

    user = User.query.get(username)
    
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

        return render_template("feedback/add.html",user=user, form=form, username=username)
    

@app.route("/feedback/<feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Shows feedback update form and allow user to update their feedback"""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        flash("Please Login First!", "danger")
        return redirect("/login")
    
    form = FeedbackForm()

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

        
    return render_template("feedback/edit.html", feedback=feedback, form=form)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Deletes user feedback"""

    feedback = Feedback.query.get_or_404(feedback_id)
    
    if "username" not in session or feedback.username != session["username"]:
        flash("Please Login First!", "danger")
        return redirect("/login")

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")



    