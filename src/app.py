from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from flask_login import LoginManager, login_user, logout_user, login_required
from config import config

# modelos
from models.ModelUser import ModelUser
from models.ModelContact import ModelContact
from models.ModelOrder import ModelOrder
from models.ModelProduct import ModelProduct

# entities:
from models.entities.User import User
from models.entities.Contact import Contact
from models.entities.Order import Order, OrderItem
from models.entities.Product import Product


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
   try:
       products = ModelProduct.get_all_products(db)
       return render_template("auth/amasijospag.html", products=products)
   except Exception as ex:
       return render_template("auth/amasijospag.html", products=[])     

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

@app.route('/admin')
@login_required
def admin_panel():
    try:
        contacts = ModelContact.get_all_contacts(db)
        orders = ModelOrder.get_all_orders(db)
        return render_template("auth/admin_panel.html", contacts=contacts, orders=orders)
    except Exception as ex:
        flash("Error al cargar el panel administrativo.")
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

@app.route('/save_order', methods=['POST'])
def save_order():
    try:
        data = request.get_json()
        
        # Datos del cliente (opcionales por ahora)
        customer_phone = data.get('phone', 'Vía WhatsApp')
        customer_name = data.get('name', 'Cliente')
        total_amount = data.get('total', 0)
        cart_items = data.get('items', [])
        
        # Crear orden
        order = Order(0, customer_phone, customer_name, total_amount)
        
        # Crear items de la orden
        items = []
        for item in cart_items:
            order_item = OrderItem(0, 0, item['name'], item['price'], 1)
            items.append(order_item)
        
        # Guardar en base de datos
        order_id = ModelOrder.save_order(db, order, items)
        
        return {'success': True, 'order_id': order_id}
        
    except Exception as ex:
        return {'success': False, 'error': str(ex)}, 400

@app.route('/orders')
@login_required
def view_orders():
    try:
        orders = ModelOrder.get_all_orders(db)
        return render_template("auth/orders.html", orders=orders)
    except Exception as ex:
        flash("Error al cargar las órdenes.")
        return redirect(url_for('home'))

@app.route('/order_details/<int:order_id>')
@login_required
def order_details(order_id):
    try:
        items = ModelOrder.get_order_details(db, order_id)
        items_data = []
        for item in items:
            items_data.append({
                'product_name': item.product_name,
                'product_price': float(item.product_price),
                'quantity': item.quantity
            })
        return {'success': True, 'items': items_data}
    except Exception as ex:
        return {'success': False, 'error': str(ex)}, 400

@app.route('/get_stock/<product_name>')
def get_stock(product_name):
    try:
        product = ModelProduct.get_by_name(db, product_name)
        if product:
            return {'success': True, 'stock': product.stock}
        else:
            return {'success': False, 'error': 'Producto no encontrado'}, 404
    except Exception as ex:
        return {'success': False, 'error': str(ex)}, 400

if __name__=='__main__':
    app.config.from_object(config['DevelopmentConfig'])
    app.run(host='0.0.0.0', port=5000, debug=True)