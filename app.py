# app.py 
from flask import Flask, render_template, request, abort, session, redirect, url_for, flash
from flask_bcrypt import Bcrypt
import os, json
import data

app = Flask(_name_)
app.secret_key = 'TU_SECRETO_SUPER_SEGURA'
bcrypt = Bcrypt(app)

# Archivo de usuarios
USERS_FILE = os.path.join('datos', 'json', 'users.json')

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    return json.load(open(USERS_FILE, encoding='utf-8'))

def save_users(u):
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(u, f, indent=2, ensure_ascii=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username'].strip()
        password = request.form['password']
        if username in users:
            flash('Usuario ya existe', 'danger')
        else:
            pw_hash = bcrypt.generate_password_hash(password).decode()
            users[username] = {'password_hash': pw_hash, 'favorites': []}
            save_users(users)
            flash('Cuenta creada. Por favor inicia sesión.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username'].strip()
        password = request.form['password']
        user = users.get(username)
        if user and bcrypt.check_password_hash(user['password_hash'], password):
            session['user'] = username
            flash(f'Bienvenido {username}!', 'success')
            return redirect(url_for('index'))
        flash('Usuario o contraseña inválida', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('index'))