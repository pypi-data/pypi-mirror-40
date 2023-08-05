import os
from flask import Flask, session
from flask_session_plus import Session
from flask_login import LoginManager, login_required, current_user
from test.auth import login_user, logout_user

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(os.path.dirname(BASE_DIR), 'firebase.json')

from test.models import User, db

app = Flask(__name__)
app.config['SESSION_CONFIG'] = [
    {
        'cookie_name': 'hola',
        'session_type': 'secure_cookie',
        'session_fields': 'auto'
    },
    {
        'cookie_name': 'fire',
        'session_type': 'firestore',
        'session_fields': ['user_id', 'user_data', '_fresh', '_id'],
        'client': db,
        'collection': 'sessions',
    }
]
app.config['SECRET_KEY'] = '_5#y7656ggu677hio'
app.config['SESION_USER_FIELDS'] = ['name', 'email', 'timezone', 'language', 'active', 'clients', 'roles']


mses = Session(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(id):
    print('USER LOADER GOT USER')
    return User.get_user_by_id(id)


@app.route('/')
def index():

    session['perro'] = True

    if 'user_id' in session:
        return f"hola: {session['user_data']}"
    else:
        return 'anon!'


@app.route('/login')
def login():
    user = User.get_user_by_id('1kuU9610nMtUlqLqdjxR')

    login_user(user)
    return 'User logged in!'


@app.route('/loginp')
def loginp():
    user = User.get_user_by_id('1kuU9610nMtUlqLqdjxR')

    login_user(user, remember=True)
    session.set_permanent('fire')

    return 'User logged in!'


@app.route('/logout')
def logout():
    logout_user()
    session.set_permanent('fire', remove=True)

    return 'User logged out!'


@app.route('/protected')
@login_required
def protected():
    return 'you have access!'


if __name__ == '__main__':
    app.run()
