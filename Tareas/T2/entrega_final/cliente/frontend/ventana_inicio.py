from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
                             QMessageBox, QHBoxLayout, QVBoxLayout)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal, QMutex
import os
from backend.logica import verificar_nombre
from parametros import ANCHO_VENTANA, LARGO_VENTANA


class Ventana_inicio(QWidget):
    senal_a_main_window = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.lock_mensaje_a_mainwindow = QMutex()
        self.inicializar_gui()

    def inicializar_gui(self):
        self.setFixedSize(ANCHO_VENTANA, LARGO_VENTANA)
        self.setWindowTitle("Conejochico: Inicio")
        self.crear_texto()
        self.crear_texto_editable()
        self.crear_boton_ingresar()
        self.crear_boton_salir()
        self.crear_logo()
        self.crear_salon_fama()
        self.setear_grilla()

    def crear_texto(self):
        self.texto = QLabel(self)
        self.texto.setText("¿Una partida?")
        self.texto.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def crear_texto_editable(self):
        self.texto_editable = QLineEdit(self)
        self.texto_editable.setPlaceholderText("Ingrese su usuario")

    def crear_boton_ingresar(self):
        self.boton_ingresar = QPushButton("&Ingresar", self)
        self.boton_ingresar.clicked.connect(self.intentar_iniciar_juego)

    def crear_boton_salir(self):
        self.boton_salir = QPushButton("&Salir", self)
        self.boton_salir.clicked.connect(
            lambda: self.mensaje_a_main_window({"boton_salir": None}))

    def crear_logo(self):
        logo = QLabel(self)
        logo.setGeometry(200, 200, 700, 119)
        ruta = os.path.join("assets", "sprites", "logo.png")
        pixeles = QPixmap(ruta)
        logo.setPixmap(pixeles)
        self.logo = QHBoxLayout()
        self.logo.addStretch()
        self.logo.addWidget(logo)
        self.logo.addStretch()

    def crear_salon_fama(self):
        self.salon_fama = QVBoxLayout()
        titulo = QLabel(self)
        titulo.setText("Salón de la Fama")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.salon_fama.addWidget(titulo)
        self.labels_fama = []
        for i in range(5):
            label = QLabel(self)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.labels_fama.append(label)
            self.salon_fama.addWidget(self.labels_fama[i])

    def setear_grilla(self):
        self.vbox_central = QVBoxLayout()
        self.hbox_botones = QHBoxLayout()
        self.hbox_botones.addStretch()
        self.hbox_botones.addWidget(self.boton_ingresar)
        self.hbox_botones.addStretch()
        self.hbox_botones.addWidget(self.boton_salir)
        self.hbox_botones.addStretch()
        self.vbox_central.addLayout(self.logo)
        self.vbox_central.addWidget(self.texto)
        self.vbox_central.addWidget(self.texto_editable)
        self.vbox_central.addLayout(self.hbox_botones)
        self.vbox_central.addLayout(self.salon_fama)
        self.setLayout(self.vbox_central)

    def intentar_iniciar_juego(self):
        nombre = self.texto_editable.text()
        if verificar_nombre(nombre):
            self.mensaje_a_main_window({"intentar_empezar_partida": nombre})
        else:
            mensaje = ("""
Por favor ingrese un nombre de usuario que:
-Sea alfanumerico
-Contenga al menos una mayuscula
-Contenga al menos un numero
-Sea de largo mayor o igual a 3 y menor o igual a 16"""
                       )
            QMessageBox.warning(self, "Error: Nombre de usuario inválido",
                                mensaje,
                                QMessageBox.StandardButton.Close,
                                QMessageBox.StandardButton.Close)

    def iniciar_juego(self):
        self.mensaje_a_main_window({"iniciar_ventana_juego": None})

    def mensaje_a_main_window(self, mensaje: dict):
        self.lock_mensaje_a_mainwindow.lock()
        self.senal_a_main_window.emit(mensaje)
        self.lock_mensaje_a_mainwindow.unlock()
