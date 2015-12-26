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

if __name__=="__main__":
    app.run(debug=True)
