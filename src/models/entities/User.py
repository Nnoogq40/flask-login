from werkzeug.security import check_password_hash 
from flask_login import UserMixin

class User(UserMixin):
    
    def __init__(self, id, username, password, fullname="") -> None:
        self.id = id
        self.username = username
        self.password = password
        self.fullname = fullname

    @classmethod
    def check_password(self,hassed_password,password):
        return check_password_hash(hassed_password, password)
    
