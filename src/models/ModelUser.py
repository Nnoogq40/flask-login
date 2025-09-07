from .entities.User import User
class ModelUser():
     @classmethod
     def login(cls, db, user):
          try:
               connection = db.connect()
               cursor = connection.cursor()
               sql = """SELECT id, username, password, fullname FROM users 
                          WHERE username = %s"""
               cursor.execute(sql, (user.username,))
               row = cursor.fetchone()
               if row is not None: 
                    authenticated_user = User(row[0], row[1], User.check_password(row[2], user.password), row[3])
                    cursor.close()
                    return authenticated_user
               else:
                    cursor.close()
                    return None
          except Exception as ex:
               raise Exception(ex)  
    
     @classmethod
     def get_by_id(cls, db, id):
          try:
               connection = db.connect()
               cursor = connection.cursor()
               sql = """SELECT id, username, fullname FROM users 
                          WHERE id = %s"""
               cursor.execute(sql, (id,))
               row = cursor.fetchone()
               if row is not None: 
                  user = User(row[0], row[1], None, row[2])
                  cursor.close()
                  return user
               else:
                    cursor.close()
                    return None
          except Exception as ex:
               raise Exception(ex)  