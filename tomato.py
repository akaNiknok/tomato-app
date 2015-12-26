from flask import Flask, render_template, request, url_for, session, redirect

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return redirect("/" + request.form["country"])
    return render_template("index.html")

@app.route("/<country>")
def country(country):
    return render_template("country.html", country=country, title=country)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pass
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        pass
    return render_template("register.html")

if __name__=="__main__":
    app.run(debug=True)
