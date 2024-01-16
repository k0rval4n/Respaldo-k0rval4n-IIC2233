from PyQt6.QtWidgets import QMessageBox, QMainWindow, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QUrl
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from frontend.ventana_inicio import Ventana_inicio
from frontend.ventana_juego import Ventana_juego
import os


class MainWindow(QMainWindow):
    senal_a_cliente = pyqtSignal(dict)
    senal_a_ventana_juego = pyqtSignal(dict)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.shortcut_inf = QShortcut(QKeySequence(Qt.Key.Key_I, Qt.Key.Key_N, Qt.Key.Key_F), self)
        self.shortcut_inf.activated.connect(self.cheat_inf)
        self.shortcut_kil = QShortcut(QKeySequence(Qt.Key.Key_K, Qt.Key.Key_I, Qt.Key.Key_L), self)
        self.shortcut_kil.activated.connect(self.cheat_kil)
        self.instanciar_audio()
        self.setFocus()
        self.jugador_moviendose = False
        self.setWindowTitle("DCConejochico")
        self.setGeometry(200, 200, 1280, 720)
        self.setFixedSize(1280, 720)
        self.ventana_inicio = Ventana_inicio()
        self.ventana_juego = None
        self.ventana_inicio.senal_a_main_window.connect(self.manejar_mensaje)
        self.setCentralWidget(self.ventana_inicio)
        self.show()

    def error_conexion(self):
        mensaje = """
Desconectado del servidor"""
        QMessageBox.warning(self, "Error: Error de conexión",
                            mensaje,
                            QMessageBox.StandardButton.Close,
                            QMessageBox.StandardButton.Close)
        self.ventana_inicio = Ventana_inicio()
        self.setCentralWidget(self.ventana_inicio)
        if self.ventana_juego is not None:
            self.ventana_juego.hide()

    def game_over(self, mensaje):
        self.derrota_mp3.play()
        self.senal_a_ventana_juego.emit({"salir_ventanajuego": None})
        label = QLabel()
        nombre = list(mensaje["game_over"])[0]
        puntaje = list(mensaje["game_over"])[1]
        mensaje = f"""
¡Has perdido!
Intentalo nuevamente {nombre} :)
Puntaje obtenido en esta partida: {round(puntaje, 2)}
"""
        label.setText(mensaje)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button = QPushButton("Salir")
        button.clicked.connect(self.salir_bonito)
        widget = QWidget()
        v_box = QVBoxLayout(widget)
        v_box.addStretch()
        v_box.addWidget(label)
        v_box.addWidget(button)
        v_box.addStretch()
        widget.setLayout(v_box)
        self.setCentralWidget(widget)

    def game_win(self, mensaje):
        self.victoria_mp3.play()
        self.senal_a_ventana_juego.emit({"salir_ventanajuego": None})
        label = QLabel()
        nombre = list(mensaje["game_win"])[0]
        puntaje = list(mensaje["game_win"])[1]
        mensaje = f"""
¡Has ganado!
Felicidades {nombre} :)
Tu puntaje es de {round(puntaje, 2)} puntos"""
        label.setText(mensaje)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button = QPushButton("Salir")
        button.clicked.connect(self.salir_bonito)
        widget = QWidget()
        v_box = QVBoxLayout(widget)
        v_box.addStretch()
        v_box.addWidget(label)
        v_box.addWidget(button)
        v_box.addStretch()
        widget.setLayout(v_box)
        self.setCentralWidget(widget)

    def usuario_bloqueado(self, mensaje):
        mensaje = (f"""
El usuario {mensaje["usuario_bloqueado"]} está sido bloqueado.
Por favor introduzca otro nombre de usuario.""")
        QMessageBox.warning(self, "Error: Usuario bloqueado",
                            mensaje,
                            QMessageBox.StandardButton.Close,
                            QMessageBox.StandardButton.Close)

    def salir_bonito(self):
        timer = QTimer()
        timer.setSingleShot(True)
        timer.start(500)
        self.close()

    def iniciar_ventana_juego(self, dict_celdas_base, dict_enemigos, dict_conejochico,
                              dict_items, dict_parametros):
        self.ventana_juego = None
        self.ventana_juego = Ventana_juego(dict_celdas_base, dict_enemigos, dict_conejochico,
                                           dict_items, dict_parametros)
        self.ventana_juego.senal_a_main_window.connect(self.manejar_mensaje)
        self.senal_a_ventana_juego.connect(self.ventana_juego.manejar_mensaje)
        if self.centralWidget() is self.ventana_inicio:
            self.ventana_inicio.hide()
        self.setCentralWidget(self.ventana_juego)
        self.jugador_moviendose = False

    def manejar_mensaje(self, mensaje: dict):
        keys = mensaje.keys()
        if "salon_de_la_fama" in keys:
            if mensaje["salon_de_la_fama"] is not None:
                for indice in range(min(5, len(mensaje["salon_de_la_fama"]))):
                    nombre_usuario, puntaje = (
                        mensaje["salon_de_la_fama"][indice])
                    txt = f"{indice + 1}.{nombre_usuario: ^16.16s}: {puntaje: ^10.2f} puntos"
                    self.ventana_inicio.labels_fama[indice].setText(txt)
                    self.ventana_inicio.labels_fama[indice].repaint()
        elif "intentar_empezar_partida" in keys:
            self.senal_a_cliente.emit(mensaje)
        elif "error_de_conexion" in keys:
            self.error_conexion()
            self.close()
        elif "usuario_bloqueado" in keys:
            self.usuario_bloqueado(mensaje)
        elif "boton_pausa" in keys:
            self.senal_a_cliente.emit(mensaje)
        elif "boton_salir" in keys:
            self.senal_a_cliente.emit(mensaje)
            if self.centralWidget() is self.ventana_juego:
                self.senal_a_ventana_juego.emit(mensaje)
            self.close()
        elif "dict_inicial" in keys:
            self.jugador_moviendose = True
            self.dict_celdas_base = mensaje["dict_inicial"]["dict_celdas_base"]
            self.dict_enemigos = mensaje["dict_inicial"]["dict_enemigos"]
            self.dict_conejochico = mensaje["dict_inicial"]["dict_conejochico"]
            self.dict_items = mensaje["dict_inicial"]["dict_items"]
            self.dict_parametros = mensaje["dict_inicial"]["dict_parametros"]
            self.iniciar_ventana_juego(self.dict_celdas_base,
                                       self.dict_enemigos, self.dict_conejochico,
                                       self.dict_items, self.dict_parametros)
            self.senal_a_cliente.emit({"cargado": None})
        elif "mover_jugador" in keys:
            self.senal_a_ventana_juego.emit(mensaje)
        elif "jugador_movido" in keys:
            self.jugador_moviendose = False
        elif "muerte" in keys or "pasar_nivel" in keys:
            self.senal_a_ventana_juego.emit(mensaje)
        elif "intentar_usar_bomba" in keys:
            self.senal_a_cliente.emit(mensaje)
        elif "mostrar_bomba" in keys:
            self.senal_a_ventana_juego.emit(mensaje)
        elif "tiempo_agotado" in keys or "boton_salir_ventanajuego" in keys:
            if self.ventana_juego is not None:
                self.ventana_juego.hide()
            self.ventana_inicio = Ventana_inicio()
            self.ventana_inicio.senal_a_main_window.connect(self.manejar_mensaje)
            self.setCentralWidget(self.ventana_inicio)
            if "boton_salir_ventanajuego" in keys:
                self.senal_a_cliente.emit(mensaje)
            self.senal_a_cliente.emit({"dame_salon_fama": None})
        elif "game_over" in keys:
            self.game_over(mensaje)
        elif "game_win" in keys:
            self.game_win(mensaje)
        else:
            self.senal_a_ventana_juego.emit(mensaje)

    def keyPressEvent(self, event):
        if isinstance(self.centralWidget(), Ventana_juego) and not self.jugador_moviendose:
            posicion_actual = tuple(
                self.ventana_juego.mapa.dict_conejochico.keys())[0]
            if event.key() == Qt.Key.Key_W and not event.isAutoRepeat():
                posicion_nueva = (posicion_actual[0] - 1, posicion_actual[1])
                self.senal_a_cliente.emit({"intentar_mover_jugador": [
                    posicion_actual, posicion_nueva]})
                self.jugador_moviendose = True
            elif event.key() == Qt.Key.Key_A and not event.isAutoRepeat():
                posicion_nueva = (posicion_actual[0], posicion_actual[1] - 1)
                self.senal_a_cliente.emit({"intentar_mover_jugador": [
                    posicion_actual, posicion_nueva]})
                self.jugador_moviendose = True
            elif event.key() == Qt.Key.Key_S and not event.isAutoRepeat():
                posicion_nueva = (posicion_actual[0] + 1, posicion_actual[1])
                self.senal_a_cliente.emit({"intentar_mover_jugador": [
                    posicion_actual, posicion_nueva]})
                self.jugador_moviendose = True
            elif event.key() == Qt.Key.Key_D and not event.isAutoRepeat():
                posicion_nueva = (posicion_actual[0], posicion_actual[1] + 1)
                self.senal_a_cliente.emit({"intentar_mover_jugador": [
                    posicion_actual, posicion_nueva]})
                self.jugador_moviendose = True
            elif event.key() == Qt.Key.Key_G and not event.isAutoRepeat():
                self.senal_a_cliente.emit({"intentar_adquirir_bomba": posicion_actual})
            elif event.key() == Qt.Key.Key_P and not event.isAutoRepeat():
                self.senal_a_ventana_juego.emit({"letra_p": None})

    def instanciar_audio(self):
        self.derrota_mp3 = QMediaPlayer(self)
        self.derrota_mp3.setAudioOutput(QAudioOutput(self))
        derrota_path = QUrl.fromLocalFile(os.path.join("assets", "sonidos", "derrota.mp3"))
        self.derrota_mp3.setSource(derrota_path)
        self.victoria_mp3 = QMediaPlayer(self)
        self.victoria_mp3.setAudioOutput(QAudioOutput(self))
        victoria_path = QUrl.fromLocalFile(os.path.join("assets", "sonidos", "victoria.mp3"))
        self.victoria_mp3.setSource(victoria_path)

    def cheat_inf(self):
        if isinstance(self.centralWidget(), Ventana_juego):
            self.senal_a_cliente.emit({"cheat_inf": None})

    def cheat_kil(self):
        if isinstance(self.centralWidget(), Ventana_juego):
            self.senal_a_cliente.emit({"cheat_kil": None})
