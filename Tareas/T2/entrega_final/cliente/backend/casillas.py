from abc import abstractmethod
from PyQt6.QtCore import QTimer, QObject, pyqtSignal, QMutex


class Casilla(QObject):
    senal_mov = pyqtSignal(tuple, tuple)

    def __init__(self, posicion):
        super().__init__()
        self.posicion = posicion
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.ejecutar)
        self.timer.setInterval(100000)

    @abstractmethod
    def __str__(self) -> str:
        return super().__str__()

    @abstractmethod
    def ejecutar(self):
        pass

    def __repr__(self):
        return str(self)

    def manejar_mensaje(self, mensaje):
        keys = mensaje.keys()
        if "start" in keys:
            self.ejecutandose = True
            self.timer.start()
        elif "stop" in keys:
            self.ejecutandose = False
            self.timer.stop()
        elif "delete" in keys:
            self.timer.killTimer(self.timer.timerId())
            self.deleteLater()

    def iniciar_timer(self):
        self.timer.start()

    def cambiar_casilla(self, nueva_posicion):
        # print(f"{self}: {QThread.currentThread()}")
        # print(f"{self}: {self.posicion} -> {nueva_posicion}")
        self.senal_mov.emit(self.posicion, nueva_posicion)

    def actualizar_posicion(self, nueva_posicion):
        self.posicion = nueva_posicion


class Casilla_vacia(Casilla):
    def __str__(self) -> str:
        return "-"

    def ejecutar(self):
        pass


class Entrada(Casilla_vacia):
    def __str__(self) -> str:
        return "E"


class Salida(Casilla_vacia):
    def __str__(self) -> str:
        return "S"


class Bomba(Casilla_vacia):
    def __init__(self, posicion, tipo):
        super().__init__(posicion)
        self.tipo = tipo

    def __str__(self) -> str:
        return f"B{self.tipo}"


class Bomba_explosion(Casilla_vacia):
    senal_terminal = pyqtSignal(tuple)

    def __init__(self, posicion, tipo, tiempo_bomba):
        super().__init__(posicion)
        self.tipo = tipo
        self._tiempo = tiempo_bomba
        self.timer.setInterval(1000)
        self.iniciar_timer()

    @property
    def tiempo(self):
        return self._tiempo

    @tiempo.setter
    def tiempo(self, x):
        if x > 0:
            self._tiempo = x
        else:
            self.senal_terminal.emit(self.posicion)
            self.timer.stop()

    def __str__(self) -> str:
        return f"X{self.tipo}"

    def ejecutar(self):
        self.tiempo -= 1


class Pared(Casilla):
    def __str__(self):
        return "P"

    def ejecutar(self):
        pass


class Canon(Pared):
    def __init__(self, posicion, direccion, velocidad):
        super().__init__(posicion)
        tiempo_disparo = int(5000 / (velocidad))
        self.timer.setInterval(tiempo_disparo)
        self.direccion = direccion

    def __str__(self):
        return f"C{self.direccion}"

    def ejecutar(self):
        self.crear_zanahoria()

    def crear_zanahoria(self):
        fila, columna = self.posicion
        if self.direccion == "U":
            self.cambiar_casilla((fila - 1, columna))
        elif self.direccion == "D":
            self.cambiar_casilla((fila + 1, columna))
        elif self.direccion == "L":
            self.cambiar_casilla((fila, columna - 1))
        elif self.direccion == "R":
            self.cambiar_casilla((fila, columna + 1))


class Entidad(Casilla):
    def __init__(self, posicion, direccion, velocidad):
        super().__init__(posicion)
        self.direccion = direccion
        self.velocidad = velocidad
        tiempo_movimiento = int(1000 / (velocidad))
        self.timer.setInterval(tiempo_movimiento)

    @abstractmethod
    def colision(self):
        pass


class Enemigo(Entidad):
    def ejecutar(self):
        self.moverse()

    def moverse(self):
        fila, columna = self.posicion
        if self.direccion == "U":
            self.cambiar_casilla((fila - 1, columna))
        elif self.direccion == "D":
            self.cambiar_casilla((fila + 1, columna))
        elif self.direccion == "L":
            self.cambiar_casilla((fila, columna - 1))
        elif self.direccion == "R":
            self.cambiar_casilla((fila, columna + 1))


class Zanahoria(Enemigo):
    def __init__(self, posicion, direccion, velocidad):
        super().__init__(posicion, direccion, velocidad)
        self.moverse()
        self.iniciar_timer()

    def __str__(self):
        return f"Z{self.direccion}"

    def colision(self):
        self.timer.stop()


class Lobo(Enemigo):
    def __init__(self, posicion, direccion, velocidad):
        super().__init__(posicion, direccion, velocidad)
        self.ralentizado = False
        if self.direccion in ["L", "R"]:
            self.tipo = "H"
        elif self.direccion in ["U", "D"]:
            self.tipo = "V"

    def __str__(self):
        return f"L{self.direccion}"

    def colision(self):
        if self.direccion == "U":
            self.direccion = "D"
        elif self.direccion == "D":
            self.direccion = "U"
        elif self.direccion == "L":
            self.direccion = "R"
        elif self.direccion == "R":
            self.direccion = "L"

    def ralentizar(self, posicion):
        if self.posicion == posicion and not self.ralentizado:
            self.ralentizado = True
            self.velocidad = 0.75 * self.velocidad
            tiempo_movimiento = int(1000 / self.velocidad)
            self.timer.setInterval(tiempo_movimiento)


class Conejochico(Entidad):
    def __init__(self, posicion, direccion, velocidad, vidas_iniciales,
                 bombas_m, bombas_c):
        super().__init__(posicion, direccion, velocidad)
        self.lock_moverse = QMutex()
        self._vidas = vidas_iniciales
        self.bomba_m = bombas_m
        self.bomba_c = bombas_c

    def __str__(self):
        return f"J{self.direccion}"

    @property
    def vidas(self):
        return self._vidas

    @vidas.setter
    def vidas(self, x):
        if x >= 0:
            self._vidas = x
        else:
            self._vidas = 0

    def perder_vida(self):
        self.vida -= 1

    def moverse(self, direccion):
        fila, columna = self.posicion
        if self.direccion == "U":
            self.cambiar_casilla((fila - 1, columna))
        elif self.direccion == "D":
            self.cambiar_casilla((fila + 1, columna))
        elif self.direccion == "L":
            self.cambiar_casilla((fila, columna - 1))
        elif self.direccion == "R":
            self.cambiar_casilla((fila, columna + 1))


class Timer_tiempo(QTimer):
    def manejar_mensaje(self, mensaje):
        keys = mensaje.keys()
        if "start" in keys:
            self.start()
        elif "stop" in keys:
            self.stop()
