from flask import Flask, render_template, request, url_for, session, redirect, make_response
import sqlite3
from os import urandom, path

ROOT = path.dirname(path.realpath(__file__))

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return redirect("/" + request.form["country"])
    if "username" in session:
        return render_template("index.html", user=session["username"])
    else:
        return render_template("index.html")

@app.route("/<country>")
def country(country):
    return render_template("country.html", country=country, title=country)

@app.route("/login", methods=["GET", "POST"])
def login():

    # Check if the user submitted the login form
    if request.method == "POST":
        form = request.form

        # Connect to the database
        db = sqlite3.connect(path.join(ROOT, "database.db"))
        # Create a cursor
        cursor = db.cursor()

        # Get the users password from the `users` table
        cursor.execute("SELECT password FROM users WHERE name=?", (form["user"],))

        # Check if the password is correct
        # If incorrect, throw an error
        try:
            if cursor.fetchone()[0] != form["pwd"]:
                db.close()
                return render_template("login.html", error=True)
        except TypeError:  # Throws a TypeError if the user is not yet registered
            db.close()
            return render_template("login.html", error=True)

        # Else, set `username` in `session` to the `user`
        session['username'] = form["user"]

        db.close()  # Close the connection
        return redirect("/")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():

    # Check if the user submitted the register form
    if request.method == "POST":
        form = request.form

        # Connect to the database
        db = sqlite3.connect(path.join(ROOT, "database.db"))
        # Create a cursor
        cursor = db.cursor()

        # Add the information to the `users` table
        cursor.execute("INSERT INTO users(name, email, password) VALUES(?,?,?)", (form["user"], form["email"], form["pwd"]))

        db.commit()  # Save the changes
        db.close()   # Close the connection

        return redirect("/")

    return render_template("register.html")

# Set the super duper secret-ish key :P
app.secret_key = urandom(24)

if __name__=="__main__":
    app.run(debug=True)
