from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton,
                             QHBoxLayout, QVBoxLayout, QGridLayout)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QMutex
from parametros import ANCHO_VENTANA, LARGO_VENTANA
from frontend.sprites import Sprite, Conejochico, Menu_inventario


class Ventana_juego(QWidget):
    senal_a_main_window = pyqtSignal(dict)
    senal_a_mapa = pyqtSignal()

    def __init__(self, dict_celdas_base, dict_enemigos, dict_conejochico,
                 dict_items, dict_parametros):
        super().__init__()
        self.setFocus()
        self.dict_parametros = dict_parametros
        self.pausa = False
        self.bomba_m_clickeada = False
        self.bomba_c_clickeada = False
        self.lock_manejar_mensaje = QMutex()
        self.lock_mensaje_a_mainwindow = QMutex()
        self.inicializar_gui(dict_celdas_base, dict_enemigos, dict_conejochico, dict_items)

    def inicializar_gui(self, dict_celdas_base, dict_enemigos, dict_conejochico, dict_items):
        self.setGeometry(200, 100, ANCHO_VENTANA, LARGO_VENTANA)
        self.setWindowTitle("Conejochico: Juego")
        self.crear_menu_lateral()
        self.crear_mapa(dict_celdas_base, dict_enemigos, dict_conejochico, dict_items)
        self.unir_menu_mapa()

    def crear_menu_lateral(self):
        self.tiempo = self.dict_parametros["DURACION_NIVEL"]
        self.vidas = self.dict_parametros["CANTIDAD_VIDAS"]
        self.menu_lateral = QVBoxLayout()
        self.label_tiempo = QLabel(self)
        self.label_tiempo.setText(f"Tiempo: {self.tiempo} segundos")
        self.label_tiempo.setFont(QFont("Arial", 20))
        self.label_vida = QLabel(self)
        self.label_vida.setText(f"Vidas restantes: {self.vidas}")
        self.label_vida.setFont(QFont("Arial", 20))
        self.crear_botones_menu_lateral()
        self.crear_menu_inventario()
        self.menu_lateral.addWidget(self.label_tiempo, alignment=Qt.AlignmentFlag.AlignCenter)
        self.menu_lateral.addWidget(self.label_vida, alignment=Qt.AlignmentFlag.AlignCenter)
        self.menu_lateral.addLayout(self.h_box_botones)
        self.menu_lateral.addWidget(self.menu_inventario)

    def crear_botones_menu_lateral(self):
        self.boton_salir = QPushButton("&Salir", self)
        self.boton_salir.clicked.connect(self.salir_ventanajuego)
        self.boton_salir.clicked.connect(
            lambda: self.senal_a_main_window.emit({"boton_salir": None}))
        self.boton_pausa = QPushButton("&Pausa", self)
        self.boton_pausa.clicked.connect(self.pausar_juego)
        self.h_box_botones = QHBoxLayout()
        self.h_box_botones.addWidget(self.boton_salir)
        self.h_box_botones.addWidget(self.boton_pausa)

    def salir_ventanajuego(self):
        self.pausar_juego()
        timer = QTimer()
        timer.setSingleShot(True)
        self.senal_a_mapa.emit()
        timer.start(5)

    def pausar_juego(self):
        if not self.pausa:
            self.pausa = True
        elif self.pausa:
            self.pausa = False
        self.mensaje_a_main_window({"boton_pausa": self.pausa})

    def crear_menu_inventario(self):
        self.menu_inventario = Menu_inventario(self.dict_parametros["BOMBAS_M"],
                                               self.dict_parametros["BOMBAS_C"])

    def crear_mapa(self, dict_celdas_base, dict_enemigos, dict_conejochico, dict_items):
        self.mapa = Mapa(self, dict_celdas_base, dict_enemigos, dict_conejochico, dict_items)
        self.senal_a_mapa.connect(self.mapa.senal_a_sprites.emit)
        self.mapa.senal_a_ventana_juego.connect(self.manejar_mensaje)
        self.repaint()

    def unir_menu_mapa(self):
        self.hbox = QHBoxLayout(self)
        self.hbox.addLayout(self.menu_lateral)
        self.hbox.addWidget(self.mapa)
        self.setLayout(self.hbox)

    def manejar_mensaje(self, mensaje: dict):
        keys = mensaje.keys()
        # self.lock_manejar_mensaje.lock()
        if "mover_jugador" in keys:
            posicion_actual = mensaje["mover_jugador"][0]
            posicion_nueva = mensaje["mover_jugador"][1]
            self.mapa.mover_sprite("J", posicion_actual, posicion_nueva)
        elif "anadir_enemigo" in keys:
            tipo, posicion_nueva, velocidad, direccion = mensaje["anadir_enemigo"]
            self.mapa.crear_enemigo(tipo, posicion_nueva, velocidad, direccion)

        elif "mover_enemigo" in keys:  # [posicion_actual, posicion_nueva]
            posicion_actual = mensaje["mover_enemigo"][0]
            posicion_nueva = mensaje["mover_enemigo"][1]
            tipo = mensaje["mover_enemigo"][2]
            self.mapa.mover_sprite(tipo, posicion_actual, posicion_nueva)
        elif "mostrar_bomba" in keys:
            tipo = mensaje["mostrar_bomba"][0]
            posicion_nueva = mensaje["mostrar_bomba"][1]
            self.mapa.colocar_bomba(tipo, posicion_nueva)

        elif "eliminar_bomba" in keys:
            posicion_actual = mensaje["eliminar_bomba"]
            self.mapa.dict_bombas[posicion_actual].setPixmap(QPixmap())
            del self.mapa.dict_bombas[posicion_actual]

        elif "eliminar_item" in keys:
            posicion_actual = mensaje["eliminar_item"]
            self.mapa.dict_items[posicion_actual].setPixmap(QPixmap())
            del self.mapa.dict_items[posicion_actual]

        elif "ralentizar_enemigo" in keys:
            posicion = mensaje["ralentizar_enemigo"]
            instancia = self.mapa.dict_enemigos[posicion]
            if instancia.ralentizado is False:
                instancia.ralentizado = True
                instancia.velocidad = (0.75 * instancia.velocidad)

        elif "TIEMPO_ACTUAL" in keys:
            tiempo = mensaje["TIEMPO_ACTUAL"]
            self.tiempo = tiempo
            self.label_tiempo.setText(f"Tiempo: {self.tiempo} segundos")
        elif "VIDA_ACTUAL" in keys:
            vidas = mensaje["VIDA_ACTUAL"]
            self.vidas = vidas
            self.label_vida.setText(f"Vidas restantes: {self.vidas}")

        elif "eliminar_enemigo" in keys:
            self.mapa.dict_enemigos[mensaje["eliminar_enemigo"]].dejar_de_moverse()
            self.mapa.dict_enemigos[mensaje["eliminar_enemigo"]].setPixmap(QPixmap())
            self.mapa.dict_enemigos[mensaje["eliminar_enemigo"]].deleteLater()
            del self.mapa.dict_enemigos[mensaje["eliminar_enemigo"]]

        elif "muerte" in keys or "pasar_nivel" in keys:
            self.senal_a_mapa.emit()
            self.hide()
            self.deleteLater()

        elif "mapa_presionado" in keys:
            if self.bomba_m_clickeada and not self.bomba_c_clickeada:
                self.mensaje_a_main_window(
                    {"intentar_usar_bomba": ["BM", mensaje["mapa_presionado"]]})
            elif self.bomba_c_clickeada and not self.bomba_m_clickeada:
                self.mensaje_a_main_window(
                    {"intentar_usar_bomba": ["BC", mensaje["mapa_presionado"]]})
        elif "actualizar_menu_inventario" in keys:
            self.menu_inventario.actualizar_menu_inventario(
                mensaje["actualizar_menu_inventario"][0], mensaje["actualizar_menu_inventario"][1])
        elif "letra_p" in keys:
            self.pausar_juego()
        elif "salir_ventanajuego" in keys:
            self.salir_ventanajuego()
        # self.lock_manejar_mensaje.unlock()

    def mensaje_a_main_window(self, mensaje: dict):
        self.lock_mensaje_a_mainwindow.lock()
        self.senal_a_main_window.emit(mensaje)
        self.lock_mensaje_a_mainwindow.unlock()

    def mousePressEvent(self, event) -> None:
        x = int(event.position().x())
        y = int(event.position().y())
        if 216 <= x <= 306:
            if 517 <= y <= 607:
                if self.bomba_m_clickeada is True:
                    self.bomba_m_clickeada = False
                elif self.bomba_m_clickeada is False:
                    self.bomba_m_clickeada = True
                self.bomba_c_clickeada = False
            elif 612 <= y <= 702:
                if self.bomba_c_clickeada is True:
                    self.bomba_c_clickeada = False
                elif self.bomba_c_clickeada is False:
                    self.bomba_c_clickeada = True
                self.bomba_m_clickeada = False
            else:
                self.bomba_m_clickeada = False
                self.bomba_c_clickeada = False
        else:
            self.bomba_m_clickeada = False
            self.bomba_c_clickeada = False
        path_m = self.menu_inventario.bomba_manzana.paths_sprites
        path_c = self.menu_inventario.bomba_congelacion.paths_sprites
        if self.bomba_m_clickeada:
            self.menu_inventario.bomba_manzana.colocar_sprite(path_m[1])
        elif not self.bomba_m_clickeada:
            self.menu_inventario.bomba_manzana.colocar_sprite(path_m[0])
        if self.bomba_c_clickeada:
            self.menu_inventario.bomba_congelacion.colocar_sprite(path_c[1])
        elif not self.bomba_c_clickeada:
            self.menu_inventario.bomba_congelacion.colocar_sprite(path_c[0])


class Mapa(QWidget):
    senal_a_sprites = pyqtSignal()
    senal_a_ventana_juego = pyqtSignal(dict)

    def __init__(self, parent=None, dict_celdas_base={}, dict_enemigos={},
                 dict_conejochico={}, dict_items={}, dict_parametros={},
                 tamano=(LARGO_VENTANA, LARGO_VENTANA)):
        super().__init__(parent)
        self.grilla_base = QGridLayout()
        self.grilla_base.setSpacing(0)
        self.grilla_base.setContentsMargins(0, 0, 0, 0)
        self.tamano = tamano
        self.tamano_sprite = (int(tamano[0] / 16), int(tamano[1] / 16))
        self.setFixedSize(*tamano)
        self.dict_enemigos = {}
        self.dict_conejochico = {}
        self.dict_items = {}
        self.dict_bombas = {}
        self.dict_extra = {}
        self.dict_parametros = dict_parametros
        self.crear_mapa_base(dict_celdas_base)
        self.crear_enemigos_base(dict_enemigos)
        self.crear_items_base(dict_items)
        self.crear_conejochico(dict_conejochico)

    def crear_items_base(self, dict_items):
        for posicion, tipo in dict_items.items():
            sprite = Sprite(self, tipo, posicion, 1)
            self.dict_items[posicion] = sprite
            self.senal_a_sprites.connect(sprite.boton_salir)

    def crear_mapa_base(self, dict_celdas_base):
        for posicion, tipo in dict_celdas_base.items():
            pos_y, pos_x = posicion
            if tipo[0] == "C":
                sprite_extra = Sprite(self, "-", posicion, 1)
                self.senal_a_sprites.connect(sprite_extra.boton_salir)
                self.dict_extra[posicion] = sprite_extra
                sprite_extra.repaint()
            sprite = Sprite(self, tipo, (0, 0), 1)
            self.grilla_base.addWidget(sprite, pos_y, pos_x)
            self.senal_a_sprites.connect(sprite.boton_salir)
        self.setLayout(self.grilla_base)

    def crear_enemigos_base(self, dict_enemigos):
        for posicion, lista in dict_enemigos.items():
            tipo = lista[0][0]
            direccion = lista[0][1]
            velocidad = lista[1]
            sprite = Sprite(self, tipo, posicion, velocidad, direccion)
            self.dict_enemigos[posicion] = sprite
            self.senal_a_sprites.connect(sprite.boton_salir)

    def crear_conejochico(self, dict_conejochico):
        for posicion, velocidad in dict_conejochico.items():
            tipo = "J"
            sprite = Conejochico(self, tipo, posicion, velocidad)
            self.dict_conejochico[posicion] = sprite
            self.senal_a_sprites.connect(sprite.boton_salir)

    def mover_sprite(self, tipo, posicion_actual, posicion_nueva):
        posicion_y = posicion_nueva[0]
        posicion_x = posicion_nueva[1]
        posicion_nueva = (posicion_y, posicion_x)
        if tipo == "J":
            instancia_sprite = self.dict_conejochico[posicion_actual]
            self.dict_conejochico[posicion_nueva] = instancia_sprite
            instancia_sprite.moverse(posicion_nueva)
            del self.dict_conejochico[posicion_actual]
        elif tipo in ["Z", "L"]:
            instancia_sprite = self.dict_enemigos[posicion_actual]
            self.dict_enemigos[posicion_nueva] = instancia_sprite
            del self.dict_enemigos[posicion_actual]
            instancia_sprite.moverse(posicion_nueva)

    def crear_enemigo(self, tipo, posicion, velocidad, direccion):
        self.dict_enemigos[posicion] = Sprite(self, tipo, posicion,
                                              velocidad, direccion)
        self.dict_enemigos[posicion].show()

    def mousePressEvent(self, event) -> None:
        x = int(event.position().x()//45)
        y = int(event.position().y()//45)
        self.senal_a_ventana_juego.emit({"mapa_presionado": (y, x)})

    def colocar_bomba(self, tipo, posicion):
        self.dict_bombas[posicion] = Sprite(self, f"X{tipo[1]}", posicion)
        self.dict_bombas[posicion].show()
