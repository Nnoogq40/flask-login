from .entities.Contact import Contact

class ModelContact():
    
    @classmethod
    def save_contact(cls, db, contact):
        try:
            connection = db.connect()
            cursor = connection.cursor()
            sql = """INSERT INTO contacts (nombre, correo, telefono, ciudad) 
                     VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (contact.nombre, contact.correo, contact.telefono, contact.ciudad))
            connection.commit()
            cursor.close()
            return True
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_all_contacts(cls, db):
        try:
            connection = db.connect()
            cursor = connection.cursor()
            sql = """SELECT id, nombre, correo, telefono, ciudad, fecha_envio 
                     FROM contacts ORDER BY fecha_envio DESC"""
            cursor.execute(sql)
            rows = cursor.fetchall()
            contacts = []
            if rows:
                for row in rows:
                    contact = Contact(row[0], row[1], row[2], row[3], row[4], row[5])
                    contacts.append(contact)
            cursor.close()
            return contacts
        except Exception as ex:
            raise Exception(ex)