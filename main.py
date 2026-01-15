from flask import Flask, render_template, request, redirect, url_for, session
import json
import hashlib
import os
import secrets

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_file = 'users.json'

def load_users():
    if not os.path.exists(user_file):
        return {}
    try:
        with open(user_file, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_users(users):
    with open(user_file, 'w') as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def send_confirmation_email(to_email, token):
    confirmation_link = f"http://127.0.0.1:5000/confirm/{token}"
    print(f"[INFO] Confirmation link for {to_email}: {confirmation_link}")

@app.route('/')
def home():
    if 'username' in session:
        return f"Hello, {session['username']}! <a href='/logout'>Logout</a>"
    return "You are not logged in. <a href='/login'>Login</a> or <a href='/register'>Register</a>"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if username in users:
            return "User exists. <a href='/register'>Try again</a>"
        token = secrets.token_urlsafe(16)
        users[username] = {
            "password": hash_password(password),
            "email": email,
            "confirmed": False,
            "token": token
        }
        save_users(users)
        send_confirmation_email(email, token)
        return "Registration successful! Check the console for the confirmation link."
    return render_template('register.html')

@app.route('/confirm/<token>')
def confirm_email(token):
    users = load_users()
    for username, info in users.items():
        if info.get("token") == token:
            info['confirmed'] = True
            info.pop('token', None)
            save_users(users)
            return f"Email confirmed! <a href='/login'>Login now</a>"
    return "Invalid or expired confirmation link."

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        if username in users:
            if users[username]['password'] == hash_password(password):
                if not users[username].get('confirmed', False):
                    return "Please confirm your email before logging in."
                session['username'] = username
                return redirect(url_for('home'))
        return "Login failed. <a href='/login'>Try again</a>"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
