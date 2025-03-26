from flask import Flask, render_template, redirect, url_for, request, session , dashboard
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session management

# Create SQLite Database and Users Table
def create_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_database()  # Ensure database is created when the app starts

@app.route('/')
def hello():
    if "user" in session:
        return f"Hello, {session['user']}! <a href='/logout'>Logout</a>"
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

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        
        # Insert into database
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                           (username, email, password))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "Error: Email already registered!"
        conn.close()


        # Redirect to a page (for example, to the homepage) after the form submission.
        return redirect(url_for('login'))
    
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user"] = user[1]  # Store username in session
            return redirect(url_for("hello"))
        else:
            return "Invalid email or password!"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("hello"))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return f"Welcome, User {session['user_id']}! This is your dashboard."
