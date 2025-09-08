from .entities.Product import Product

class ModelProduct():
    
    @classmethod
    def get_all_products(cls, db):
        try:
            connection = db.connect()
            cursor = connection.cursor()
            sql = "SELECT id, name, price, stock, description, image_url FROM products ORDER BY name"
            cursor.execute(sql)
            rows = cursor.fetchall()
            products = []
            if rows:
                for row in rows:
                    product = Product(row[0], row[1], row[2], row[3], row[4], row[5])
                    products.append(product)
            cursor.close()
            return products
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_by_name(cls, db, name):
        try:
            connection = db.connect()
            cursor = connection.cursor()
            sql = "SELECT id, name, price, stock, description, image_url FROM products WHERE name = %s"
            cursor.execute(sql, (name,))
            row = cursor.fetchone()
            product = None
            if row:
                product = Product(row[0], row[1], row[2], row[3], row[4], row[5])
            cursor.close()
            return product
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def update_stock(cls, db, product_name, quantity_sold):
        try:
            connection = db.connect()
            cursor = connection.cursor()
            sql = "UPDATE products SET stock = stock - %s WHERE name = %s AND stock >= %s"
            cursor.execute(sql, (quantity_sold, product_name, quantity_sold))
            if cursor.rowcount == 0:
                raise Exception(f"Stock insuficiente para {product_name}")
            connection.commit()
            cursor.close()
            return True
        except Exception as ex:
            connection.rollback()
            cursor.close()
            raise Exception(ex)
    
    @classmethod
    def check_stock_availability(cls, db, items):
        """Verifica si hay stock suficiente para todos los items"""
        try:
            connection = db.connect()
            cursor = connection.cursor()
            
            for item in items:
                sql = "SELECT stock FROM products WHERE name = %s"
                cursor.execute(sql, (item.product_name,))
                row = cursor.fetchone()
                if not row:
                    raise Exception(f"Producto {item.product_name} no encontrado")
                if row[0] < item.quantity:
                    raise Exception(f"Stock insuficiente para {item.product_name}. Disponible: {row[0]}, Solicitado: {item.quantity}")
            
            cursor.close()
            return True
        except Exception as ex:
            cursor.close()
            raise Exception(ex)