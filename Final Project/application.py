import os
import locale

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from Predict import Predict
import tensorflow

import logging
import sys
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


db = SQL("sqlite:///heart.db")
@app.route("/", methods=["GET", "POST"])
def main():
    return render_template("main.html")

@app.route("/more", methods=["GET", "POST"])
@login_required
def more():
    # Directs the user to the more html when they try to open it
    if request.method == "GET":
        return render_template("more.html")

    # Takes care of the code as the user is trying to fill out the form

    else:
        # A list to collect the inputs from the user
        X = []

        # Extract the age the user's inputs
        age = request.form.get("age")

        # if the user fails to input an age renders a page that instructs them to do so
        if age == "":
            return apology("Age can not be empty", 403)

        # cast the age the user inputted (which is a string at this point) into a float
        age = float(age)

        # addds the age to list that is going to be used to predict
        X.append(age)

        # Extract the sex the user's inputs
        sex = request.form.get("sex")

        # if the user fails to input an age renders a page that instructs them to do so
        if sex == "":
            return apology("The 'sex' field can not be empty", 403)

        # cast the sex the user inputted (which is a string at this point) into a float
        sex = float(sex)

        # addds the sex to list
        X.append(sex)

        # Extract the weight the user's inputs
        weight = request.form.get("weight")
        # if the user fails to input a weight renders a page that instructs them to do so
        if weight == "":
            return apology("The wieght field can not be empty", 403)

        # Extract the chest the user's inputs
        chest = request.form.get("chest")

        # if the user fails to input anything, renders a page that instructs them to do so
        if chest == "":
            return apology("The 'Chest pain' field can not be empty", 403)

        # cast the input(which is a string at this point) into a float
        chest = float(chest)

        # addds the input to list that is going to be used to predict
        X.append(chest)

        # Extract the input
        rbp = request.form.get("rbp")
        # renders a page that instructs the user to input a valid input if they fail to do so
        if rbp == "":
            rbp = request.form.get("checkrbp")
            if rbp == "":
                return apology("The 'Resting blood pressure' field can not be empty. If you don't know your results, check the 'I don't know' box", 403)

        # cast the input(which is a string at this point) into a float
        rbp = float(rbp)

        # addds the input to list that is going to be used to predict
        X.append(rbp)

        # Extracts the input and adds it to the list to be used for predicition
        chol = request.form.get("chol")

        # renders a page that instructs the user to input a valid input if they fail to do so
        if chol == "":
            chol = request.form.get("checkchol")
            if chol == "":
                return apology("The 'Cholestrol' field can not be empty. If you don't know your results, check the 'I don't know' box", 403)

        # cast the input(which is a string at this point) into a float
        chol = float(chol)
        X.append(chol)

        # Extract the age the user's inputs
        fbs = request.form.get("fbs")

        # renders a page that instructs the user to input a valid input if they fail to do so
        if fbs == "":
            fbs = request.form.get("checkfbs")
            if fbs == "":
                return apology("The 'Fasting Blood Sugar' field can not be empty. If you don't know your results, check the 'I don't know' box", 403)

        # cast the input(which is a string at this point) into a float
        fbs = float(fbs)
        X.append(fbs)

        # Extract the input and adds it to a list used for prediction
        rer = request.form.get("rer")
        if rer == "":
            return apology("The 'Electrocardiographic Result' field can not be empty.", 403)

        # cast the input(which is a string at this point) into a float
        rer = float(rer)
        X.append(rer)

        # Extracts the input and adds it to the list
        mhr = request.form.get("mhr")
        # renders a page that instructs the user to input a valid input if they fail to do so
        if mhr == "":
            mhr = request.form.get("checkmhr")
            if mhr == "":
                return apology("The 'Maximum Heart Rate' field can not be empty. If you don't know your results, check the 'I don't know' box", 403)

        # cast the input(which is a string at this point) into a float
        if mhr is None:
            return apology("The 'Maximum Heart Rate' field can not be empty. If you don't know your results, check the 'I don't know' box", 403)
        mhr = float(mhr)
        X.append(mhr)

        # Extract the input from the user and appends it to list that is used to predict
        eia = request.form.get("eia")
        if eia == "":
                return apology("The 'Indused Angina' field can not be empty.", 403)
        eia = float(eia)
        X.append(eia)

        # Extract the input from the user and adds it to the list used for prediction
        st = request.form.get("st")

        # renders a page that instructs the user to input a valid input if they fail to do so
        if st == "":
            st = request.form.get("checkst")
            if st == "":
                return apology("The 'ST depression result' field can not be empty. If you don't know your results, check the 'I don't know' box", 403)

        # cast the input(which is a string at this point) into a float
        st = float(st)
        X.append(st)

        # Extract the input and adds it to the list used for predicition
        slope = request.form.get("slope")

        # renders a page that instructs the user to input a valid input if they fail to do so
        if slope == "":
            return apology("The 'Slope' field can not be empty.", 403)

        # cast the input(which is a string at this point) into a float
        slope = float(slope)
        X.append(slope)

        # Extract the input and adds it to the list used for predicition
        vessel = request.form.get("vessel")

        # renders a page that instructs the user to input a valid input if they fail to do so
        if vessel == "":
            return apology("The 'Vessel' field can not be empty.", 403)

        # cast the input(which is a string at this point) into a float
        vessel = float(vessel)
        X.append(vessel)

        # Extract the input from the user and adds it to the list used for prediction
        thal = request.form.get("thal")

        # renders a page that instructs the user to input a valid input if they fail to do so
        if thal == "":
            return apology("The 'Thal' field can not be empty.", 403)

        # cast the input(which is a string at this point) into a float
        thal = float(thal)
        X.append(thal)

        # Calls the predict function from Predict.py onto the list that is now a compiliation of all of the user's inputs
        Y = Predict(X)
        Y = Y * 100
        Y = round(Y, 2)

        if Y < 50:
        	# Passes the prediction (the result is in percents) to result.html
        	return render_template("result.html", Y=Y)
        else:
        	return render_template("result50.html", Y=Y)

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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/more")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""


    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # checks if user is trying to register
    if request.method == "POST":

        # ensures the user types in a username
        username = request.form.get("username")
        if not username:
            return apology("must provide username", 403)

        # ensures that the user types in a password
        password = request.form.get("password")
        if not password:
            return apology("must provide password", 403)

        # ensures that the user confirms their password
        confirm_password = request.form.get("confirm_password")
        if not confirm_password:
            return apology("must confirm password")

        # ensures the password and the confirmation are the same
        if password != confirm_password:
            return apology("Password must match", 403)

        # retrieves the database
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)

        # checks if the username already exists in the database
        if len(rows) != 0:
            return apology("Username has been used. Try again", 403)

        # hashes the password to store into the database
        hash_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        # stores the hashed password and the username into the database
        db.execute("INSERT INTO users (username, hash) VALUES(:username, :password)", username=username, password=hash_password)

        # ***remember the user's session
        new_user_id = db.execute("SELECT id FROM users WHERE username = :username", username=username)
        session["user_id"] = new_user_id

        # allows the user to log in
        return redirect("/login")

    # Checks if user is visiting site to access the register page
    else:
        return render_template("register.html")


if __name__ == "__main__":
    app.run()
