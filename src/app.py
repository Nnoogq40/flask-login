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

@app.route('/erp')
@login_required
def erp_dashboard():
    try:
        # Obtener datos para el dashboard
        contacts = ModelContact.get_all_contacts(db)
        orders = ModelOrder.get_all_orders(db)
        products = ModelProduct.get_all_products(db)
        
        # Obtener datos financieros
        cursor = db.connection.cursor()
        
        # Empleados
        cursor.execute("SELECT * FROM employees WHERE activo = true ORDER BY fecha_contratacion DESC")
        employees_data = cursor.fetchall()
        employees = []
        for emp in employees_data:
            employees.append({
                'id': emp[0], 'nombre': emp[1], 'cargo': emp[2], 
                'salario': emp[3], 'telefono': emp[4], 'email': emp[5],
                'fecha_contratacion': emp[6], 'activo': emp[7]
            })
        
        # Proveedores
        cursor.execute("SELECT * FROM suppliers ORDER BY fecha_registro DESC")
        suppliers_data = cursor.fetchall()
        suppliers = []
        for sup in suppliers_data:
            suppliers.append({
                'id': sup[0], 'nombre': sup[1], 'empresa': sup[2],
                'telefono': sup[3], 'email': sup[4], 'direccion': sup[5]
            })
        
        # Transacciones
        cursor.execute("SELECT * FROM transactions ORDER BY fecha_transaccion DESC LIMIT 20")
        transactions_data = cursor.fetchall()
        transactions = []
        for trans in transactions_data:
            transactions.append({
                'id': trans[0], 'tipo': trans[1], 'descripcion': trans[2],
                'monto': trans[3], 'categoria': trans[4], 'fecha_transaccion': trans[5]
            })
        
        # Calcular totales financieros
        cursor.execute("SELECT SUM(monto) FROM transactions WHERE tipo = 'ingreso' AND fecha_transaccion >= CURRENT_DATE - INTERVAL '30 days'")
        total_ingresos = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT SUM(monto) FROM transactions WHERE tipo = 'gasto' AND fecha_transaccion >= CURRENT_DATE - INTERVAL '30 days'")
        total_gastos = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT COUNT(*) FROM employees WHERE activo = true")
        total_empleados = cursor.fetchone()[0] or 0
        
        cursor.close()
        
        return render_template("auth/erp_dashboard.html", 
                             contacts=contacts, orders=orders, products=products,
                             employees=employees, suppliers=suppliers, transactions=transactions,
                             total_ingresos=total_ingresos, total_gastos=total_gastos, 
                             total_empleados=total_empleados)
    except Exception as ex:
        flash("Error al cargar el dashboard ERP.")
        return redirect(url_for('home'))

@app.route('/add_employee', methods=['POST'])
@login_required
def add_employee():
    try:
        # Obtener datos del formulario
        nombre = request.form['nombre']
        cargo = request.form['cargo']
        salario = float(request.form['salario'])
        telefono = request.form.get('telefono', '')
        email = request.form.get('email', '')
        fecha_contratacion = request.form.get('fecha_contratacion')
        
        # Insertar en base de datos
        cursor = db.connection.cursor()
        cursor.execute("""
            INSERT INTO employees (nombre, cargo, salario, telefono, email, fecha_contratacion)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nombre, cargo, salario, telefono, email, fecha_contratacion))
        db.connection.commit()
        cursor.close()
        
        return {'success': True}
    except Exception as ex:
        return {'success': False, 'error': str(ex)}, 400

@app.route('/add_supplier', methods=['POST'])
@login_required
def add_supplier():
    try:
        # Obtener datos del formulario
        nombre = request.form['nombre']
        empresa = request.form['empresa']
        telefono = request.form.get('telefono', '')
        email = request.form.get('email', '')
        direccion = request.form.get('direccion', '')
        
        # Insertar en base de datos
        cursor = db.connection.cursor()
        cursor.execute("""
            INSERT INTO suppliers (nombre, empresa, telefono, email, direccion)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, empresa, telefono, email, direccion))
        db.connection.commit()
        cursor.close()
        
        return {'success': True}
    except Exception as ex:
        return {'success': False, 'error': str(ex)}, 400

@app.route('/add_transaction', methods=['POST'])
@login_required
def add_transaction():
    try:
        # Obtener datos del formulario
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        monto = float(request.form['monto'])
        categoria = request.form.get('categoria', 'otros')
        fecha_transaccion = request.form.get('fecha_transaccion')
        metodo_pago = request.form.get('metodo_pago', 'efectivo')
        
        # Insertar en base de datos
        cursor = db.connection.cursor()
        cursor.execute("""
            INSERT INTO transactions (tipo, descripcion, monto, categoria, fecha_transaccion, metodo_pago)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (tipo, descripcion, monto, categoria, fecha_transaccion, metodo_pago))
        db.connection.commit()
        cursor.close()
        
        return {'success': True}
    except Exception as ex:
        return {'success': False, 'error': str(ex)}, 400

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
        
        # Registrar venta como ingreso en el sistema financiero
        try:
            cursor = db.connection.cursor()
            productos_lista = ", ".join([item['name'] for item in cart_items])
            descripcion = f"Venta #{order_id} - {productos_lista}"
            cursor.execute("""
                INSERT INTO transactions (tipo, descripcion, monto, categoria, metodo_pago)
                VALUES (%s, %s, %s, %s, %s)
            """, ('ingreso', descripcion, total_amount, 'ventas', 'efectivo'))
            db.connection.commit()
            cursor.close()
        except Exception as ex:
            print(f"Error registrando transacción financiera: {ex}")
        
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