# Darran Shivdat
# This code simulates a journal site
# Parts are adapted or taken from cs50 Finance
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash


from helpers import apology, login_required
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


db = SQL("sqlite:///journal.db")

# From CS50 FInance
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.route("/")
@login_required
def home():
    return render_template("home.html")

# Handling with errors

# Taken from CS50 Finance
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# Taken from CS50 Finance
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        # Field Checking
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation password", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
             return apology("Passwords do not match", 400)
        # If the username is unique than hash the password, otherwise return apology
        else:
            if len(db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))) == 0:
                # Definitions
                user = request.form.get("username")
                passhash = generate_password_hash(request.form.get("password"))
                # Inserting the new username and password hash into the users database
                key = db.execute("INSERT INTO users(username,hash) VALUES (:username, :hash)",username = user,hash = passhash)
                session["user_id"] = key
                return redirect ("/")
            else:
                return apology("Username already taken", 400)

    return render_template ("register.html")

@login_required
@app.route("/journal", methods=["GET", "POST"])
def journal():
    if request.method == "POST":
        # Ensuring the field are filled
        if not request.form.get("journal"):
            return apology("must provide entry", 400)

        if not request.form.get("title"):
            return apology("must provide title", 400)


        entry = request.form.get("journal")
        post_title = request.form.get("title")

        db.execute("UPDATE users SET entries = entries +1")


        # Darran reflection test

        q1 = request.form.get("question1")
        q2 = request.form.get("question2")
        q3 = request.form.get("question3")
        q4 = request.form.get("question4")
        q5 = request.form.get("question5")
        q6 = request.form.get("question6")
        q7 = request.form.get("question7")


        if not q1:
            return apology("must answer question", 400)
        if not q2:
            return apology("must answer question", 400)
        if not q3:
            return apology("must answer question", 400)
        if not q4:
            return apology("must answer question", 400)
        if not q5:
            return apology("must answer question", 400)
        if not q6:
            return apology("must answer question", 400)
        if not q7:
            return apology("must answer question", 400)

        DRA = int(q1) + int(q2) + int(q3) + int(q4) + int(q5) + int(q6) + int(q7)


        db.execute("INSERT INTO entries (entry, title, user_id, DRA) VALUES(:entry,:post_title,:user_id, :DRA)",
                      entry = entry, post_title = post_title, user_id=session["user_id"], DRA = DRA)

        flash ("Journal Entry Successfully Entered!")

        return redirect("/history")
    else:
        return render_template("journal.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    entries = db.execute('''SELECT * FROM entries WHERE
                            user_id = :user_id''', user_id = session['user_id'])

    if len(entries) == 0:
        return render_template("empty.html")
    else:
        return render_template("history.html", entries=entries)

@app.route("/viewpost/<id>")
@login_required
def viewpost(id):


    journal_post = db.execute('''SELECT * FROM entries WHERE
                            id = :id''', id = id)

    return render_template("viewpost.html", journal_post=journal_post[0])



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)