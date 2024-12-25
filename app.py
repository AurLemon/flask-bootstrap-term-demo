from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def renderTemplate(page):
    return render_template(
        page,
        bootstrap_css=url_for('static', filename='bootstrap/css/bootstrap.min.css'),
        bootstrap_js=url_for('static', filename='bootstrap/js/bootstrap.bundle.js')
    )

@app.route("/")
def indexView():
    return renderTemplate("index.html")

@app.route("/admin")
def adminView():
    return renderTemplate("views/admin.html")

@app.route("/blog")
def blogView():
    return renderTemplate("views/blog.html")

@app.route("/login")
def loginView():
    return renderTemplate("views/login.html")

if __name__ == "__main__":
    app.run(debug=True)