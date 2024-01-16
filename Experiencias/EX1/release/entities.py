class Usuario:
    def __init__(self):
        self.suscripcion = False
        self.canasta = []
        self._puntos = 0

    def agregar_item(self, item):
        self.canasta.append(item)
        if self.suscripcion == True:
            item.

    def comprar(self):
        
usuario = Usuario()
class Item:
    def __init__(self):
        self.nombre = ""
        self.puntos = 0
        self._precio = 0