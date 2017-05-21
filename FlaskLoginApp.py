from functools import wraps

import gc
from flask_login import user_loaded_from_header, login_user, LoginManager, UserMixin, user_logged_in, user_logged_out
from flask import g, Flask, request, redirect, abort, Response, render_template, flash, session, url_for

app = Flask(__name__)

app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="users.login"

class User(UserMixin):
    def __init__(self, id,username="admin",password="password"):
        self.id = id
        self.name=username
      #  self.password=self.name+"_secret"
        self.password=password

    def get_id(self):
        return self.id

    def __repr__(self):
        return "%d %s %s" %(self.id,self.name
                            ,self.password)

#users = [User(id) for id in range(1,21)]

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('loginLatest.html')
    else:
        return "Hello Boss ! <a href='/logout'>logout</a>"

@app.route('/login', methods = ['POST'])
def adminlogin():
    username = request.form['username']
    password = request.form['password']
       # id = username.split(':')[1]
    if username == 'admin' and password == 'password':
        session['logged_in']=True
        user= User(username,password,4)
        login_user(user)
       # user_logged_in(user)
       # flash('User is logged in successfully')
        #    next = request.args.get('main')
        #    return render_template('login.html')
    else:
        flash('Please enter correct username and password')
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
   # user_logged_out(user)
    flash("You have been logged out")
  #  gc.collect()
    return home()



@login_manager.user_loader
def load_user(id):
    return User(id)

@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')

if __name__ == '__main__':
    app.run()
