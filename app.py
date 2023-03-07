from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)
app.secret_key = 'mysecretkey'

login_manager = LoginManager()
login_manager.init_app(app)

users = {'user1': {'password': 'password'},
         'user2': {'password': 'password'}}

messages = []

class User(UserMixin):
    def __init__(self, id_, password):
        self.id = id_
        self.password = password

    def __repr__(self):
        return f'<User: {self.id}>'

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id, users[user_id]['password'])
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and password == users[username]['password']:
            user = User(username, password)
            login_user(user)
            return redirect(url_for('home'))
        else:
            return 'Invalid username/password combination'
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    return render_template('index.html', messages=messages)

@app.route('/post', methods=['POST'])
@login_required
def post():
    messages.append(request.form['message'])
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
