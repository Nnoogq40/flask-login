class Order:
    
    def __init__(self, id, customer_phone, customer_name, total_amount, status='pending', fecha_orden=None):
        self.id = id
        self.customer_phone = customer_phone
        self.customer_name = customer_name
        self.total_amount = total_amount
        self.status = status
        self.fecha_orden = fecha_orden


class OrderItem:
    
    def __init__(self, id, order_id, product_name, product_price, quantity=1):
        self.id = id
        self.order_id = order_id
        self.product_name = product_name
        self.product_price = product_price
        self.quantity = quantity