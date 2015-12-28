from flask import Flask, render_template, request, url_for, session, redirect, make_response
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return redirect("/" + request.form["country"])
    return render_template("index.html", user=request.cookies.get("username"))

@app.route("/<country>")
def country(country):
    return render_template("country.html", country=country, title=country)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = request.form

        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute("SELECT password FROM users WHERE name=?", (form["user"],))
        if cursor.fetchone()[0] != form["pwd"]:
            db.close()
            return render_template("login.html", error=True)

        resp = make_response(redirect("/"))
        resp.set_cookie("username", form["user"])
        db.close()
        return resp
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        form = request.form

        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute("INSERT INTO users(name, email, password) VALUES(?,?,?)", (form["user"], form["email"], form["pwd"]))
        db.commit()
        db.close()

        return redirect("/")
    return render_template("register.html")

if __name__=="__main__":
    app.run(debug=True)
