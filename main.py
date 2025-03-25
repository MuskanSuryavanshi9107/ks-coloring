from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/home')
def home():
    return redirect(url_for("hello"))  # Redirecting to the '/' route

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run(debug=True)
