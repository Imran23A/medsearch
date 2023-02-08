import hashlib
import subprocess
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, make_response, session, flash
from flask_babel import Babel
from flask_babel import gettext as _


app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_DEFAULT_FOLDER'] = 'translations'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['LANGUAGES'] = {
    'en': 'English',
    'ru': 'Russian',
}

babel = Babel(app)

def get_locale():
    language = session.get('language')
    if language and language in app.config['LANGUAGES']:
        return language
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


babel.init_app(app, locale_selector=get_locale)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    hashed_password = hash_password(password)
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, hashed_password))
    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def validate_user(username,password):
    user = get_user(username)
    if user:
        hashed_password = user[2]
        if hashed_password == hash_password(password):
            return True
    return False

@app.route('/')
def index():
    language = session.get('language', 'en')

    if 'username' in session:
        username = session['username'] # check if needed username, lang and locale
        return render_template('index.html', username=username)
    return render_template('index.html', language=language)

@app.route('/set_language/<string:language>', methods=['POST'])
def set_language(language):
    session['language'] = language
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        action = request.form.get('action')
    if action == "Register":
        # Get the values from the form
        username = request.form['username']
        password = request.form['password']
        # Validate the user input
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif get_user(username):
            error = 'User {} is already registered.'.format(username)
        elif len(password) < 8:
            error = 'Password must be at least 8 characters long.'
        elif not any(c.isupper() for c in password):
            error = 'Password must contain at least one uppercase letter.'
        elif not any(c.isdigit() for c in password):
            error = 'Password must contain at least one number.'

        if error is None:
            create_user(username, password)
            session['username'] = username
            return redirect(url_for('index'))

        flash(error)
    elif action == "Login":
        # Get the values from the form
        username = request.form['username']
        password = request.form['password']

        # Validate the user input
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not validate_user(username,password):
            error = 'Incorrect username or password.'

        if error is None:
            session['username'] = username
            return redirect(url_for('index'))
        flash(error)
    return render_template('index.html')

@app.route('/deregister', methods=['POST'])
def deregister():
    if 'username' in session:
        username = session['username']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        conn.close()
        session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/search', methods=['POST'])
def search():
    query = request.form['search']
    result = subprocess.run(['esearch', '-db', 'pubmed', '-query', query], capture_output=True, text=True)
    return render_template('search_results.html', result=result.stdout)

if __name__ == '__main__':
    app.run(debug=True)


