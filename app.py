# app.py
from flask import Flask, render_template, request, abort, session, redirect, url_for, flash
from flask_bcrypt import Bcrypt
import os, json
import data

app = Flask(_name_)
app.secret_key = 'TU_SECRETO_SUPER_SEGURA'  # Cámbialo por uno fuerte en producción
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