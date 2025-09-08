class Contact:
    
    def __init__(self, id, nombre, correo, telefono, ciudad, fecha_envio=None):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.ciudad = ciudad
        self.fecha_envio = fecha_envio