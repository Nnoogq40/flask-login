from .entities.Order import Order, OrderItem
from .ModelProduct import ModelProduct

class ModelOrder():
    
    @classmethod
    def save_order(cls, db, order, items):
        connection = None
        cursor = None
        try:
            # Verificar stock disponible antes de procesar la orden
            ModelProduct.check_stock_availability(db, items)
            
            connection = db.connect()
            cursor = connection.cursor()
            
            # Insertar orden principal
            sql_order = """INSERT INTO orders (customer_phone, customer_name, total_amount, status) 
                          VALUES (%s, %s, %s, %s) RETURNING id"""
            cursor.execute(sql_order, (order.customer_phone, order.customer_name, order.total_amount, order.status))
            order_id = cursor.fetchone()[0]
            
            # Insertar los productos de la orden y reducir stock
            for item in items:
                sql_item = """INSERT INTO order_items (order_id, product_name, product_price, quantity) 
                             VALUES (%s, %s, %s, %s)"""
                cursor.execute(sql_item, (order_id, item.product_name, item.product_price, item.quantity))
                
                # Reducir stock del producto
                ModelProduct.update_stock(db, item.product_name, item.quantity)
            
            connection.commit()
            if cursor:
                cursor.close()
            return order_id
        except Exception as ex:
            if connection:
                connection.rollback()
            if cursor:
                cursor.close()
            raise Exception(ex)
    
    @classmethod
    def get_all_orders(cls, db):
        try:
            connection = db.connect()
            cursor = connection.cursor()
            sql = """SELECT o.id, o.customer_phone, o.customer_name, o.total_amount, o.status, o.fecha_orden,
                            COUNT(oi.id) as total_items
                     FROM orders o 
                     LEFT JOIN order_items oi ON o.id = oi.order_id
                     GROUP BY o.id, o.customer_phone, o.customer_name, o.total_amount, o.status, o.fecha_orden
                     ORDER BY o.fecha_orden DESC"""
            cursor.execute(sql)
            rows = cursor.fetchall()
            orders = []
            if rows:
                for row in rows:
                    order = Order(row[0], row[1], row[2], row[3], row[4], row[5])
                    order.total_items = row[6]
                    orders.append(order)
            cursor.close()
            return orders
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_order_details(cls, db, order_id):
        try:
            connection = db.connect()
            cursor = connection.cursor()
            sql = """SELECT id, order_id, product_name, product_price, quantity 
                     FROM order_items WHERE order_id = %s"""
            cursor.execute(sql, (order_id,))
            rows = cursor.fetchall()
            items = []
            if rows:
                for row in rows:
                    item = OrderItem(row[0], row[1], row[2], row[3], row[4])
                    items.append(item)
            cursor.close()
            return items
        except Exception as ex:
            raise Exception(ex)