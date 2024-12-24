from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def indexView():
    return render_template(
        "index.html",
        bootstrap_css=url_for('static', filename='bootstrap/css/bootstrap.min.css'),
        bootstrap_js=url_for('static', filename='bootstrap/js/bootstrap.bundle.js')
    )

@app.route("/admin")
def adminView():
    return render_template("views/admin.html")

@app.route("/blog")
def blogView():
    return render_template("views/blog.html")

@app.route("/login")
def loginView():
    return render_template("views/login.html")

if __name__ == "__main__":
    app.run(debug=True)