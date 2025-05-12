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

@app.route('/favorites')
def favorites():
    if 'user' not in session:
        return redirect(url_for('login'))
    users = load_users()
    favs = users[session['user']]['favorites']
    datos = data.cargar_datos()
    revistas_fav = {t: datos[t] for t in favs if t in datos}
    return render_template('favorites.html', revistas=revistas_fav)

@app.route('/toggle_fav/<nombre>')
def toggle_fav(nombre):
    if 'user' not in session:
        return redirect(url_for('login'))
    users = load_users()
    favs = users[session['user']]['favorites']
    if nombre in favs:
        favs.remove(nombre)
        flash(f'"{nombre}" eliminado de favoritos', 'warning')
    else:
        favs.append(nombre)
        flash(f'"{nombre}" agregado a favoritos', 'success')
    save_users(users)
    return redirect(request.referrer or url_for('index'))

@app.route('/areas')
def areas():
    base = data.cargar_base()
    areas = sorted({a for rev in base.values() for a in rev.get('areas', [])})
    return render_template('areas.html', areas=areas)

@app.route('/areas/<area>')
def area_detalle(area):
    revistas = data.filtrar_por_area(area)
    if not revistas:
        abort(404)
    return render_template('revistas.html', revistas=revistas, titulo=f"Área: {area}")

@app.route('/catalogos')
def catalogos():
    base = data.cargar_base()
    catalogos = sorted({c for rev in base.values() for c in rev.get('catalogos', [])})
    return render_template('catalogos.html', catalogos=catalogos)

@app.route('/catalogos/<cat>')
def catalogo_detalle(cat):
    revistas = data.filtrar_por_catalogo(cat)
    if not revistas:
        abort(404)
    return render_template('revistas.html', revistas=revistas, titulo=f"Catálogo: {cat}")

@app.route('/explorar')
def explorar():
    iniciales = sorted({t[0].upper() for t in data.cargar_base().keys()})
    return render_template('explorar.html', iniciales=iniciales)

@app.route('/explorar/<letra>')
def explorar_letra(letra):
    revistas = data.filtrar_por_inicial(letra)
    if not revistas:
        abort(404)
    return render_template('revistas.html', revistas=revistas, titulo=f"Revistas que inician con '{letra.upper()}'")