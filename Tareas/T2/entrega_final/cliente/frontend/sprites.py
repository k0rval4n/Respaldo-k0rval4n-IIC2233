from PyQt6.QtWidgets import (QWidget, QLabel, QHBoxLayout, QVBoxLayout)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QTimer, QMutex, QPropertyAnimation, QPoint
from backend.obtener_paths import obtener_paths_sprites


class Sprite(QLabel):
    def __init__(self, parent=None, tipo=None, posicion=(0, 0), velocidad=1,
                 direccion="", tamano=(45, 45)):
        super().__init__(parent)
        self.lock_moverse = QMutex()
        self.contador = 0
        self.velocidad = velocidad
        self.posicion = (posicion[0] * 45, posicion[1] * 45)  # pos real!
        self.tamano = tamano
        args = (self.posicion[1], self.posicion[0]) + self.tamano
        self.setGeometry(*args)
        self.setFixedSize(*tamano)
        self.tipo = tipo
        self.direccion = direccion
        if tipo != "J":
            self.paths_sprites = self.obtener_paths(f"{self.tipo}{self.direccion}")
            self.n_sprites = len(self.paths_sprites)
            self.colocar_sprite(self.paths_sprites[0])
        self.indice_paths = 0
        self.moviendose = False
        self.timer_animacion = QTimer()
        self.timer_animacion.setInterval(200)
        self.timer_animacion.timeout.connect(self.animacion)
        self.timer_animacion.start()
        self.ralentizado = False

    def animacion(self):
        if len(self.paths_sprites) > 1:
            if self.moviendose:
                self.indice_paths = (self.indice_paths + 1) % self.n_sprites
                path = self.paths_sprites[self.indice_paths]
                self.colocar_sprite(path)
                self.repaint()
            elif self.indice_paths != 0:
                self.colocar_sprite(self.paths_sprites[0])
                self.indice_paths = 0
                self.repaint()

    def colocar_sprite(self, path):
        self.pixeles = QPixmap(path)
        self.setPixmap(self.pixeles)
        self.setScaledContents(True)

    def obtener_paths(self, tipo):
        return obtener_paths_sprites(tipo)

    def moverse(self, nueva_posicion):
        n_pos_y = nueva_posicion[0]
        n_pos_x = nueva_posicion[1]
        delta_y = int((45 * n_pos_y - self.posicion[0]) / 45)
        delta_x = int((45 * n_pos_x - self.posicion[1]) / 45)
        self.movimiento = QPropertyAnimation(self, b"pos")
        self.movimiento.setDuration(int(1000 / self.velocidad))
        self.movimiento.setStartValue(QPoint(self.posicion[1], self.posicion[0]))
        self.movimiento.setEndValue(QPoint(nueva_posicion[1] * 45, nueva_posicion[0] * 45))
        self.movimiento.finished.connect(self.dejar_de_moverse)
        self.moviendose = True
        if delta_y > 0:
            self.direccion = "D"
        elif delta_y < 0:
            self.direccion = "U"
        elif delta_x > 0:
            self.direccion = "R"
        elif delta_x < 0:
            self.direccion = "L"
        self.paths_sprites = self.obtener_paths(f"{self.tipo}{self.direccion}")
        self.colocar_sprite(self.paths_sprites[0])
        self.indice_paths = 0
        self.repaint()
        self.movimiento.start()
        self.posicion = (n_pos_y * 45, n_pos_x * 45)

    def dejar_de_moverse(self):
        self.moviendose = False

    def cambiar_direccion(self, direccion):
        self.direccion = direccion
        self.paths_sprites = self.obtener_paths(f"{self.tipo}{self.direccion}")
        self.n_sprites = len(self.paths_sprites)
        self.colocar_sprite(self.paths_sprites[0])

    def boton_salir(self):
        self.timer_animacion.stop()


class Conejochico(Sprite):
    def __init__(self, parent=None, tipo=None, posicion=(0, 0), velocidad=1, tamano=(45, 45)):
        super().__init__(parent, tipo, posicion, velocidad, tamano)
        self.direccion = "R"
        self.path_R = self.obtener_paths("JR")
        self.path_L = self.obtener_paths("JL")
        self.path_U = self.obtener_paths("JU")
        self.path_D = self.obtener_paths("JD")
        self.paths_sprites = self.path_R
        self.colocar_sprite(self.paths_sprites[0])

    def animacion(self):
        if len(self.paths_sprites) > 1:
            if self.moviendose:
                if self.direccion == "R":
                    self.paths_sprites = self.path_R
                elif self.direccion == "L":
                    self.paths_sprites = self.path_L
                elif self.direccion == "U":
                    self.paths_sprites = self.path_U
                elif self.direccion == "D":
                    self.paths_sprites = self.path_D
                self.n_sprites = len(self.paths_sprites)
                self.indice_paths = (self.indice_paths + 1) % self.n_sprites
                path = self.paths_sprites[self.indice_paths]
                self.colocar_sprite(path)
                self.repaint()
            elif self.indice_paths != 0:
                self.colocar_sprite(self.paths_sprites[0])
                self.indice_paths = 0
                self.repaint()


class Menu_inventario(QWidget):
    def __init__(self, bombas_m=0, bombas_c=0):
        super().__init__(None)
        self.bomba_manzana = Sprite(self, "BM", (0, 0), 1, "", (90, 90))
        self.label_BM = QLabel()
        self.label_BM.setFont(QFont("Arial", 20))
        self.h_box_manzana = QHBoxLayout()
        self.h_box_manzana.addWidget(self.bomba_manzana)
        self.h_box_manzana.addWidget(self.label_BM)

        self.bomba_congelacion = Sprite(self, "BC", (0, 0), 1, "", (90, 90))
        self.label_BC = QLabel()
        self.label_BC.setFont(QFont("Arial", 20))
        self.h_box_congelacion = QHBoxLayout()
        self.h_box_congelacion.addWidget(self.bomba_congelacion)
        self.h_box_congelacion.addWidget(self.label_BC)

        self.label_inventario = QLabel()
        self.label_inventario.setText("Inventario")
        self.label_inventario.setFont(QFont("Arial", 20))

        self.v_box_inventario = QVBoxLayout()
        self.v_box_inventario.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.v_box_inventario.addWidget(self.label_inventario,
                                        alignment=Qt.AlignmentFlag.AlignCenter)
        self.v_box_inventario.addLayout(self.h_box_manzana)
        self.v_box_inventario.addLayout(self.h_box_congelacion)
        self.setLayout(self.v_box_inventario)
        self.actualizar_menu_inventario(bombas_m, bombas_c)

    def actualizar_menu_inventario(self, cant_BM: int, cant_BC: int):
        self.label_BM.setText(str(cant_BM))
        self.label_BC.setText(str(cant_BC))
