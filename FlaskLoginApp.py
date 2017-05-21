from functools import wraps

from flask_login import login_user, LoginManager, UserMixin, logout_user
from flask import g, Flask, request, Response, render_template, flash, session, url_for

app = Flask(__name__)

app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="users.login"

class User(UserMixin):
    def __init__(self, id,username="admin@editorlabs.com",password="password"):
        self.id = id
        self.name=username
        self.password=password

    def get_id(self):
        return self.id

    def __repr__(self):
        return "%d %s %s" %(self.id,self.name
                            ,self.password)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss ! <a href='/logout'>logout</a>"

@app.route('/login', methods = ['POST'])
def adminlogin():
    username = request.form['Email address']
    password = request.form['Password']
    if username == 'admin@editorlabs.com' and password == 'password':
        session['logged_in']=True
        user= User(username,password,4)
        login_user(user)
    else:
        flash('Please enter correct email address and password')
    return home()

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return home()

    return wrap

@app.route("/logout/")
@login_required
def logout():
    session['logged_in'] = False
    logout_user()
    flash("You have been logged out")
    return home()



@login_manager.user_loader
def load_user(id):
    return User(id)

@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')

if __name__ == '__main__':
    app.run()
