from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from flask_login import LoginManager, login_user, logout_user, login_required
from config import config

# modelos
from models.ModelUser import ModelUser
from models.ModelContact import ModelContact

# entities:
from models.entities.User import User
from models.entities.Contact import Contact


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

@app.route('/submit', methods=['POST'])
def submit_contact():
    try:
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form['telefono']
        ciudad = request.form['ciudad']
        
        # Crear objeto Contact
        contact = Contact(0, nombre, correo, telefono, ciudad)
        
        # Guardar en la base de datos
        ModelContact.save_contact(db, contact)
        
        flash("¡Mensaje enviado correctamente! Pronto nos pondremos en contacto contigo.")
        return redirect(url_for('home'))
        
    except Exception as ex:
        flash("Error al enviar el mensaje. Por favor intenta de nuevo.")
        return redirect(url_for('home'))

@app.route('/contacts')
@login_required
def view_contacts():
    try:
        contacts = ModelContact.get_all_contacts(db)
        return render_template("auth/contacts.html", contacts=contacts)
    except Exception as ex:
        flash("Error al cargar los contactos.")
        return redirect(url_for('home'))

if __name__=='__main__':
    app.config.from_object(config['DevelopmentConfig'])
    app.run(host='0.0.0.0', port=5000, debug=True)