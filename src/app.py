from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from flask_login import LoginManager, login_user, logout_user, login_required
from config import config

# modelos
from models.ModelUser import ModelUser

# entities:
from models.entities.User import User


app = Flask(__name__)

# PostgreSQL connection setup
class DatabaseConnection:
    def __init__(self, app):
        self.app = app
        self.connection = None
        
    def connect(self):
        if self.connection is None or self.connection.closed:
            self.connection = psycopg2.connect(self.app.config['DATABASE_URL'])
        return self.connection

db = DatabaseConnection(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
   return ModelUser.get_by_id(db,id)
   
@app.route("/")
def index():
   return  redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
     #print(request.form['username'])
     #print(request.form['password'])
     user = User(0,request.form['username'],request.form['password'])
     logged_user= ModelUser.login(db,user)
     if logged_user != None:
        if logged_user.password:
           login_user(logged_user)
           return redirect(url_for('home'))
        else:
           flash("invdalid password.....")
           return render_template('auth/login.html')  
     else:
        flash("user not found.....")
        return render_template('auth/login.html')   
    else:
     return render_template('auth/login.html')
@app.route('/home')
def home():
   return render_template("auth/amasijospag.html")     


if __name__=='__main__':
    app.config.from_object(config['DevelopmentConfig'])
    app.run(host='0.0.0.0', port=5000, debug=True)