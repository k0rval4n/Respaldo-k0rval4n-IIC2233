from backend.tablero import Tablero
from backend.obtener_paths import obtener_paths_tableros
from PyQt6.QtCore import QThread, pyqtSignal, QMutex
from parametros import PUNTAJE_LOBO, PUNTAJE_INF, DICT_PARAMETROS_INICIALES


class Partida(QThread):
    senal_a_tablero = pyqtSignal(dict)
    senal_a_cliente = pyqtSignal(dict)

    def __init__(self, nivel):
        super().__init__()
        self.dict_parametros_iniciales = DICT_PARAMETROS_INICIALES
        self.uso_chetos = False
        self.lock_enviar_mensaje_a_cliente = QMutex()
        self.lock_enviar_mensaje_a_tablero = QMutex()
        self.lock_pasar_nivel = QMutex()
        self.lock_manejar_mensaje = QMutex()
        self._nivel = 1
        self.nivel = nivel
        self.velocidad_conejo = self.dict_parametros_iniciales["VELOCIDAD_CONEJO"]
        self.velocidad_zanahoria = self.dict_parametros_iniciales["VELOCIDAD_ZANAHORIA"]
        self.tiempo_bomba = self.dict_parametros_iniciales["TIEMPO_BOMBA"]
        self.estoy_pausado = False

    def run(self):
        self.exec()

    @property
    def nivel(self):
        return self._nivel

    @nivel.setter
    def nivel(self, x):
        if 1 <= x <= 3:
            self._nivel = x
        elif x < 1:
            self._nivel = 1
        elif x > 3:
            self._nivel = 3

    def iniciar_tablero(self, tiempo=None, vidas=None, muerto=False, bombas_m=None, bombas_c=None):
        if tiempo is None:
            duracion_nivel = self.calcular_duracion_nivel(self.nivel)
        else:
            duracion_nivel = tiempo
        velocidad_lobo = self.calcular_vel_lobo(self.nivel)
        tamano = (
            self.dict_parametros_iniciales["LARGO_LABERINTO"],
            self.dict_parametros_iniciales["ANCHO_LABERINTO"])
        dict_parametros = dict(self.dict_parametros_iniciales)
        del dict_parametros["DURACION_NIVEL_INICIAL"]
        del dict_parametros["VELOCIDAD_LOBO_INICIAL"]
        dict_parametros["DURACION_NIVEL"] = duracion_nivel
        dict_parametros["VELOCIDAD_LOBO"] = velocidad_lobo
        if vidas is None:
            dict_parametros["CANTIDAD_VIDAS"] = (
                max(1, dict_parametros["CANTIDAD_VIDAS"] - self.nivel + 1))
        else:
            dict_parametros["CANTIDAD_VIDAS"] = vidas
        if bombas_m is not None:
            dict_parametros["BOMBAS_M"] = bombas_m
        if bombas_c is not None:
            dict_parametros["BOMBAS_C"] = bombas_c
        self.enviar_msg_a_cliente({"parametros_tablero": dict_parametros})
        self.tablero_nivel = Tablero(self.cargar_tablero(muerto), tamano,
                                     dict_parametros)
        self.tablero_nivel.senal_a_partida.connect(self.manejar_mensaje)
        self.senal_a_tablero.connect(self.tablero_nivel.manejar_mensaje)
        self.enviar_msg_a_tablero({"start": None})
        if self.uso_chetos:
            self.enviar_msg_a_tablero({"cheat_inf": None})

    def pasar_de_nivel(self):
        self.lock_pasar_nivel.lock()
        if self.nivel < 3:
            tiempo_restante = self.tablero_nivel.tiempo
            conejochico = list(self.tablero_nivel.dict_conejochicho.values())[0]
            vidas_restantes = conejochico.vidas
            bombas_m = conejochico.bomba_m
            bombas_c = conejochico.bomba_c
            cant_lobos_eliminados = self.tablero_nivel.lobos_eliminados
            puntaje_nivel = 0
            if cant_lobos_eliminados > 0:
                puntaje_nivel = round((tiempo_restante * vidas_restantes) /
                                      (cant_lobos_eliminados * PUNTAJE_LOBO), 2)
            if self.uso_chetos:
                puntaje_nivel = PUNTAJE_INF
            self.enviar_msg_a_cliente({"pasar_nivel": [self.nombre_usuario,
                                                       self.nivel,
                                                       puntaje_nivel]})
            self.nivel += 1
            self.senal_a_tablero.disconnect()
            self.uso_chetos = False
            self.iniciar_tablero(self.calcular_duracion_nivel(self.nivel),
                                 vidas_restantes, False, bombas_m, bombas_c)
        else:
            tiempo_restante = self.tablero_nivel.tiempo
            vidas_restantes = list(self.tablero_nivel.dict_conejochicho.values())[0].vidas
            cant_lobos_eliminados = self.tablero_nivel.lobos_eliminados
            puntaje_nivel = 0
            if cant_lobos_eliminados > 0:
                puntaje_nivel = round((tiempo_restante * vidas_restantes) /
                                      (cant_lobos_eliminados * PUNTAJE_LOBO), 2)
            if self.uso_chetos:
                puntaje_nivel = PUNTAJE_INF
            self.enviar_msg_a_cliente({"game_win": [self.nombre_usuario,
                                                    self.nivel,
                                                    puntaje_nivel]})
        self.lock_pasar_nivel.unlock()

    def calcular_duracion_nivel(self, nivel):
        if nivel <= 1:
            return self.dict_parametros_iniciales["DURACION_NIVEL_INICIAL"]
        else:
            return (self.calcular_duracion_nivel(nivel - 1) *
                    self.dict_parametros_iniciales["PONDERADOR_LABERINTO"])

    def calcular_vel_lobo(self, nivel):
        if nivel == 1:
            return self.dict_parametros_iniciales["VELOCIDAD_LOBO_INICIAL"]
        else:
            return (self.calcular_vel_lobo(nivel - 1) /
                    self.dict_parametros_iniciales["PONDERADOR_LABERINTO"])

    def cargar_tablero(self, muerto=False):
        path = obtener_paths_tableros()[self.nivel - 1]
        with open(path, "r", encoding="utf-8") as file:
            tablero = file.readlines()
            tablero_16x16 = []
            for i in range(DICT_PARAMETROS_INICIALES["LARGO_LABERINTO"]):
                linea = tablero[i].strip().strip(",").split(",")
                if muerto and "C" in linea:
                    linea[linea.index("C")] = "-"
                if muerto and "E" in linea:
                    linea[linea.index("E")] = "C"
                tablero_16x16.append(linea)
            return tablero_16x16

    def enviar_msg_a_cliente(self, mensaje: dict):
        self.lock_enviar_mensaje_a_cliente.lock()
        self.senal_a_cliente.emit(mensaje)
        self.lock_enviar_mensaje_a_cliente.unlock()

    def enviar_msg_a_tablero(self, mensaje: dict):
        self.lock_enviar_mensaje_a_tablero.lock()
        self.senal_a_tablero.emit(mensaje)
        self.lock_enviar_mensaje_a_tablero.unlock()

    def manejar_mensaje(self, mensaje: dict):
        # if self.lock_manejar_mensaje.tryLock():
        keys = mensaje.keys()
        if "empezar_partida" in keys:
            self.nombre_usuario = mensaje["empezar_partida"][1]
            self.nivel = mensaje["empezar_partida"][0]
            self.iniciar_tablero()
        elif "boton_salir" in keys:
            self.enviar_msg_a_tablero({"boton_salir": None})
            self.terminar()
        elif "intentar_usar_bomba" in keys:
            self.enviar_msg_a_tablero(mensaje)
        elif "boton_pausa" in keys:
            self.enviar_msg_a_tablero(mensaje)
        elif "dict_inicial" in keys:
            self.enviar_msg_a_cliente(mensaje)
        elif "mover_jugador" in keys or "mostrar_bomba" in keys or \
                "eliminar_bomba" in keys or "mover_enemigo" in keys or \
                "anadir_enemigo" in keys or "eliminar_enemigo" in keys or \
                "eliminar_item" in keys:
            self.enviar_msg_a_cliente(mensaje)
        elif "dict_parametros" in keys:
            self.dict_parametros = mensaje["dict_parametros"]
        elif "TIEMPO_ACTUAL" in keys:
            self.enviar_msg_a_cliente(mensaje)
        elif "salida" in keys:
            self.pasar_de_nivel()
        elif "muerte" in keys:
            if mensaje["muerte"][0] <= 0:
                # self.enviar_msg_a_cliente(mensaje)
                self.enviar_msg_a_cliente({"game_over": None})
            else:
                self.enviar_msg_a_cliente(mensaje)
                self.senal_a_tablero.disconnect()
                self.iniciar_tablero(self.calcular_duracion_nivel(self.nivel),
                                     mensaje["muerte"][0], True)
        elif "jugador_movido" in keys:
            self.enviar_msg_a_cliente(mensaje)
        elif "intentar_adquirir_bomba" in keys:
            self.enviar_msg_a_tablero(mensaje)
        elif "actualizar_menu_inventario" in keys:
            self.enviar_msg_a_cliente(mensaje)
        elif "ralentizar_enemigo" in keys:
            self.enviar_msg_a_cliente(mensaje)
        elif "cheat_inf" in keys:
            self.uso_chetos = True
            self.enviar_msg_a_tablero(mensaje)
        elif "cheat_kil" in keys:
            self.enviar_msg_a_tablero(mensaje)
        else:
            self.enviar_msg_a_tablero(mensaje)
        # self.lock_manejar_mensaje.unlock()

    def terminar(self):
        self.quit()
        self.wait()
