from PyQt6.QtCore import QTimer, QThread, pyqtSignal, QMutex
from random import randint
from backend.casillas import (Casilla_vacia, Entrada, Salida, Bomba, Bomba_explosion, Pared,
                              Canon, Zanahoria, Lobo, Conejochico, Timer_tiempo)


class Tablero(QThread):
    senal_com_casillas = pyqtSignal(dict)
    senal_a_partida = pyqtSignal(dict)
    senal_ralentizar = pyqtSignal(tuple)

    def __init__(self, tablero: list, tamano: tuple, dict_parametros: dict):
        super().__init__()
        self.tablero, self.tamano, self.dict_parametros = [tablero, tamano, dict_parametros]
        self.bombas_anterior, self.bomba_adquirible = [None, False]
        self.lock_salida, self.lobos_eliminados = [QMutex(), 0]
        self._tiempo = int(dict_parametros["DURACION_NIVEL"])
        self.dict_locks_casillas = {}
        self.lock_enviar_mensaje, self.lock_manejar_mensaje = [QMutex(), QMutex()]
        self.dict_celdas_base = {}
        self.dict_enemigos = {}
        self.dict_items = {}
        self.dict_bombas = {}
        self.dict_conejochicho = {}
        self.estoy_pausado, self.cheat_inf = [False, False]

    def run(self):
        self.ejecutar()
        self.exec()

    @property
    def tiempo(self):
        return self._tiempo

    @tiempo.setter
    def tiempo(self, x):
        if self.cheat_inf is not True:
            if x > 0:
                self._tiempo = int(x)
            else:
                self._tiempo = 0
                instancia = list(self.dict_conejochicho.values())[0]
                instancia.vidas -= 1
                self.enviar_mensaje({"muerte": [instancia.vidas, self.tiempo]})
                self.terminar()
        else:
            self._tiempo = self._tiempo

    def ejecutar(self):
        self.crear_locks_casillas()
        self.crear_tablero(self.tablero)
        self.crear_contador_tiempo()
        dict_inicial = (
            {"dict_celdas_base": {clave: str(valor) for clave, valor in
                                  self.dict_celdas_base.items()},
             "dict_enemigos": {clave: [str(valor), valor.velocidad] for clave, valor in
                               self.dict_enemigos.items()},
             "dict_items": {clave: str(valor) for clave, valor in self.dict_items.items()},
             "dict_bombas": {clave: str(valor) for clave, valor in self.dict_bombas.items()},
             "dict_conejochico": {clave: valor.velocidad for clave, valor in
                                  self.dict_conejochicho.items()},
             "dict_parametros": self.dict_parametros})
        self.enviar_mensaje({"dict_inicial": dict_inicial})

    def crear_locks_casillas(self):
        for posicion in [(x, y) for x in range(self.tamano[1]) for y in range(self.tamano[0])]:
            self.dict_locks_casillas[posicion] = QMutex()

    def crear_tablero(self, tablero_lista):
        for fila in range(self.tamano[0]):
            for columna in range(self.tamano[1]):
                string = tablero_lista[fila][columna]
                posicion = fila, columna
                instancia = self.transformar_casilla(posicion, string)
                if string == "C":
                    self.dict_conejochicho[posicion] = instancia
                    self.dict_celdas_base[posicion] = (self.transformar_casilla(posicion, "-"))
                elif string[0] in ["C", "-", "E", "S", "P"]:
                    self.dict_celdas_base[posicion] = instancia
                elif string[0] == "B":
                    self.dict_items[posicion] = instancia
                    self.dict_celdas_base[posicion] = (self.transformar_casilla(posicion, "-"))
                elif string[0] == "X":
                    self.dict_bombas[posicion] = instancia
                    self.dict_celdas_base[posicion] = (self.transformar_casilla(posicion, "-"))
                elif string[0] == "L":
                    self.dict_enemigos[posicion] = instancia
                    self.dict_celdas_base[posicion] = (self.transformar_casilla(posicion, "-"))

    def transformar_casilla(self, posicion, string):
        if string == "C":
            dic = self.dict_parametros
            instancia = Conejochico(posicion, "R", dic["VELOCIDAD_CONEJO"], dic["CANTIDAD_VIDAS"],
                                    dic["BOMBAS_M"], dic["BOMBAS_C"])
            self.senal_com_casillas.connect(instancia.manejar_mensaje)
            instancia.senal_mov.connect(self.cambiar_casilla)
        elif string[0] == "B":
            instancia = Bomba(posicion, string[1])
            self.senal_com_casillas.connect(instancia.manejar_mensaje)
            instancia.senal_mov.connect(self.cambiar_casilla)
        elif string == "E":
            instancia = Entrada(posicion)
            self.senal_com_casillas.connect(instancia.manejar_mensaje)
            instancia.senal_mov.connect(self.cambiar_casilla)
        elif string == "S":
            instancia = Salida(posicion)
            self.senal_com_casillas.connect(instancia.manejar_mensaje)
            instancia.senal_mov.connect(self.cambiar_casilla)
        elif string[0] == "C":
            instancia = Canon(posicion, string[1], self.dict_parametros["VELOCIDAD_ZANAHORIA"])
            self.senal_com_casillas.connect(instancia.manejar_mensaje)
            instancia.senal_mov.connect(self.cambiar_casilla)
        elif string[0] == "Z":
            instancia = Zanahoria(posicion, string[1], self.dict_parametros["VELOCIDAD_ZANAHORIA"])
            self.senal_com_casillas.connect(instancia.manejar_mensaje)
            instancia.senal_mov.connect(self.cambiar_casilla)
        elif string[0] == "L":
            direccion_int = randint(0, 1)
            if string[1] == "H":
                direccion = ["L", "R"][direccion_int]
            elif string[1] == "V":
                direccion = ["U", "D"][direccion_int]
            instancia = Lobo(posicion, direccion, self.dict_parametros["VELOCIDAD_LOBO"])
            self.senal_com_casillas.connect(instancia.manejar_mensaje)
            instancia.senal_mov.connect(self.cambiar_casilla)
            self.senal_ralentizar.connect(instancia.ralentizar)
        elif string == "-":
            instancia = Casilla_vacia(posicion)
            self.senal_com_casillas.connect(instancia.manejar_mensaje)
            instancia.senal_mov.connect(self.cambiar_casilla)
        elif string[0] == "X":
            instancia = Bomba_explosion(posicion, string[1], self.dict_parametros["TIEMPO_BOMBA"])
            self.senal_com_casillas.connect(instancia.manejar_mensaje)
            instancia.senal_mov.connect(self.cambiar_casilla)
            instancia.senal_terminal.connect(self.eliminar_bomba)
        else:
            instancia = Pared(posicion)
            self.senal_com_casillas.connect(instancia.manejar_mensaje)
            instancia.senal_mov.connect(self.cambiar_casilla)
        return instancia

    def cambiar_casilla(self, posicion_actual, posicion_nueva):
        if self.validar_movimiento(posicion_nueva):
            self.dict_locks_casillas[posicion_nueva].lock()
            if posicion_actual in self.dict_conejochicho.keys():
                self.cambiar_casilla_jugador(posicion_nueva)
            elif posicion_actual in self.dict_enemigos.keys() and \
                    isinstance(self.dict_enemigos[posicion_actual], Zanahoria) and \
                    posicion_nueva in self.dict_enemigos.keys():
                instancia = self.dict_enemigos[posicion_actual]
                self.enviar_mensaje({"eliminar_enemigo": posicion_actual})
                del self.dict_enemigos[posicion_actual]
                instancia.colision()
            elif posicion_actual in self.dict_enemigos.keys() and \
                    isinstance(self.dict_enemigos[posicion_actual], Lobo) and \
                    posicion_nueva in self.dict_enemigos.keys() and \
                    isinstance(self.dict_enemigos[posicion_nueva], Lobo):
                instancia = self.dict_enemigos[posicion_actual]
                instancia.colision()
            elif posicion_actual in self.dict_enemigos.keys() and \
                    posicion_nueva not in self.dict_enemigos.keys():
                self.cambiar_casilla_enemigo(posicion_actual, posicion_nueva)
            elif posicion_actual in self.dict_celdas_base.keys() and \
                    isinstance(self.dict_celdas_base[posicion_actual], Canon):
                instancia = self.dict_celdas_base[posicion_actual]
                direccion = instancia.direccion
                self.enviar_mensaje({"anadir_enemigo": ["Z", posicion_nueva,
                                     self.dict_parametros["VELOCIDAD_ZANAHORIA"], direccion]})
                self.dict_enemigos[posicion_nueva] = self.transformar_casilla(
                    posicion_nueva, f"Z{direccion}")
            self.dict_locks_casillas[posicion_nueva].unlock()
            return True
        elif posicion_actual in self.dict_enemigos.keys():
            instancia = self.dict_enemigos[posicion_actual]
            if isinstance(instancia, Zanahoria):
                self.enviar_mensaje({"eliminar_enemigo": posicion_actual})
                del self.dict_enemigos[posicion_actual]
            instancia.colision()
        return False

    def cambiar_casilla_enemigo(self, pos_actual, pos_nueva):
        instancia_enemigo = self.dict_enemigos[pos_actual]
        tipo = str(instancia_enemigo)[0]
        self.enviar_mensaje({"mover_enemigo": [(pos_actual), (pos_nueva), tipo]})
        del self.dict_enemigos[pos_actual]
        self.dict_enemigos[pos_nueva] = instancia_enemigo
        instancia_enemigo.actualizar_posicion(pos_nueva)

    def cambiar_casilla_jugador(self, posicion_nueva):
        posicion_actual = list(self.dict_conejochicho.keys())[0]
        instancia_jugador = self.dict_conejochicho[posicion_actual]
        self.dict_conejochicho[posicion_nueva] = instancia_jugador
        del self.dict_conejochicho[posicion_actual]

    def validar_movimiento(self, posicion):
        fil, col = posicion
        mov_valido = (0 <= fil < self.tamano[0] and 0 <= col < self.tamano[1]
                      and not isinstance(self.dict_celdas_base[posicion], Pared))
        return mov_valido

    def crear_contador_tiempo(self):
        self.timer_contador_tiempo = Timer_tiempo()
        self.timer_contador_tiempo.setInterval(1000)
        self.timer_contador_tiempo.timeout.connect(self.restar_tiempo)
        self.senal_com_casillas.connect(self.timer_contador_tiempo.manejar_mensaje)
        self.timer_posicion = Timer_tiempo()
        self.timer_posicion.setInterval(100)
        self.timer_posicion.timeout.connect(self.verificar_posicion)
        self.senal_com_casillas.connect(self.timer_posicion.manejar_mensaje)

    def restar_tiempo(self):
        self.tiempo -= 1
        self.enviar_mensaje({"TIEMPO_ACTUAL": self.tiempo})

    def enviar_mensaje(self, mensaje: dict):
        self.lock_enviar_mensaje.lock()
        self.senal_a_partida.emit(mensaje)
        self.lock_enviar_mensaje.unlock()

    def manejar_mensaje(self, mensaje: dict):
        keys = mensaje.keys()
        if "start" in keys:
            self.start()
            self.bombas_anterior = list(mensaje.values())[0]
        elif "cargado" in keys:
            self.senal_com_casillas.emit({"start": None})
        elif "boton_salir" in keys:
            self.terminar()
        elif "desconexion" in keys:
            self.terminar()
        if "intentar_mover_jugador" in keys:
            if self.estoy_pausado is False:
                tiempo = int(1000 / self.dict_parametros["VELOCIDAD_CONEJO"])
                posicion_actual, posicion_nueva = mensaje["intentar_mover_jugador"]
                n_pos_y, n_pos_x = posicion_nueva[0], posicion_nueva[1]
                delta_y = n_pos_y - posicion_actual[0]
                delta_x = n_pos_x - posicion_actual[1]
                if delta_y > 0:
                    direccion = "D"
                elif delta_y < 0:
                    direccion = "U"
                elif delta_x > 0:
                    direccion = "R"
                elif delta_x < 0:
                    direccion = "L"
                self.timer_conejo = QTimer()
                self.timer_conejo.setInterval(tiempo)
                self.timer_conejo.timeout.connect(lambda: self.mover_conejo(direccion))
                self.senal_com_casillas.connect(self.timer_conejo.stop)
                self.mover_conejo(direccion)
                self.timer_conejo.start()
        elif "intentar_usar_bomba" in keys:
            tipo, posicion = mensaje["intentar_usar_bomba"]
            if self.validar_movimiento(posicion):
                self.colocar_bomba(posicion, tipo)
        elif "intentar_adquirir_bomba" in keys:
            self.adquirir_bomba(mensaje["intentar_adquirir_bomba"])
        elif "boton_pausa" in keys:
            if self.estoy_pausado is False:
                self.estoy_pausado = True
                self.senal_com_casillas.emit({"stop": None})
            elif self.estoy_pausado is True:
                self.estoy_pausado = False
                self.senal_com_casillas.emit({"start": None})
        elif "cheat_kil" in keys:
            self.senal_com_casillas.emit({"stop": None})
            for pos_casilla in list(self.dict_celdas_base.keys()):
                if isinstance(self.dict_celdas_base[pos_casilla], Canon):
                    self.dict_celdas_base[pos_casilla].deleteLater()
                    del self.dict_celdas_base[pos_casilla]
            for pos_enemigo in list(self.dict_enemigos.keys()):
                if isinstance(self.dict_enemigos[pos_enemigo], Zanahoria):
                    self.enviar_mensaje({"eliminar_enemigo": pos_enemigo})
                    self.dict_enemigos[pos_enemigo].deleteLater()
                    del self.dict_enemigos[pos_enemigo]
                else:
                    self.eliminar_lobo(pos_enemigo)
            self.senal_com_casillas.emit({"start": None})
        elif "cheat_inf" in keys:
            self.cheat_inf = True

    def mover_conejo(self, direccion):
        posicion_actual = list(self.dict_conejochicho.keys())[0]
        if direccion == "D":
            posicion_nueva = (posicion_actual[0] + 1, posicion_actual[1])
        elif direccion == "U":
            posicion_nueva = (posicion_actual[0] - 1, posicion_actual[1])
        elif direccion == "R":
            posicion_nueva = (posicion_actual[0], posicion_actual[1] + 1)
        elif direccion == "L":
            posicion_nueva = (posicion_actual[0], posicion_actual[1] - 1)
        es_valido = self.validar_movimiento(posicion_nueva)
        if es_valido:
            mensaje = {"mover_jugador": [posicion_actual, posicion_nueva]}
            self.enviar_mensaje(mensaje)
            self.cambiar_casilla(posicion_actual, posicion_nueva)
        if not es_valido:
            self.enviar_mensaje({"jugador_movido": None})
            self.timer_conejo.stop()

    def verificar_posicion(self):
        posicion_jugador = list(self.dict_conejochicho.keys())[0]
        casilla = self.dict_celdas_base[posicion_jugador]
        if posicion_jugador in self.dict_enemigos.keys():
            instancia = self.dict_conejochicho[posicion_jugador]
            if self.cheat_inf is not True:
                instancia.vidas -= 1
            self.enviar_mensaje({"muerte": [instancia.vidas, self.tiempo]})
            self.terminar()
        elif isinstance(casilla, Salida):
            self.enviar_mensaje({"salida": None})
            self.terminar()
        for posicion in self.dict_bombas.keys():
            if posicion in self.dict_enemigos.keys():
                if self.dict_bombas[posicion].tipo == "M":
                    self.eliminar_lobo(posicion)
                elif self.dict_bombas[posicion].tipo == "C":
                    self.ralentizar_lobo(posicion)

    def colocar_bomba(self, posicion, tipo):
        dale = False
        if list(self.dict_conejochicho.values())[0].bomba_m > 0 and tipo == "BM":
            dale = True
            list(self.dict_conejochicho.values())[0].bomba_m -= 1
        elif list(self.dict_conejochicho.values())[0].bomba_c > 0 and tipo == "BC":
            dale = True
            list(self.dict_conejochicho.values())[0].bomba_c -= 1
        if dale:
            self.enviar_mensaje(
                {"actualizar_menu_inventario": [list(self.dict_conejochicho.values())[0].bomba_m,
                                                list(self.dict_conejochicho.values())[0].bomba_c]})
            set_posiciones_validas = set()
            fila, columna = posicion
            valido_u, valido_d, valido_l, valido_r = [True, True, True, True]
            tamano_y, tamano_x = self.tamano
            for delta_y in range(0, tamano_y):
                if self.validar_movimiento((fila + delta_y, columna)) and valido_d:
                    set_posiciones_validas.add((fila + delta_y, columna))
                else:
                    valido_d = False
                if self.validar_movimiento((fila - delta_y, columna)) and valido_u:
                    set_posiciones_validas.add((fila - delta_y, columna))
                else:
                    valido_u = False
            for delta_x in range(0, tamano_x):
                if self.validar_movimiento((fila, columna + delta_x)) and valido_r:
                    set_posiciones_validas.add((fila, columna + delta_x))
                else:
                    valido_r = False
                if self.validar_movimiento((fila, columna - delta_x)) and valido_l:
                    set_posiciones_validas.add((fila, columna - delta_x))
                else:
                    valido_l = False
            for pos_valida in set_posiciones_validas:
                if pos_valida in self.dict_bombas.keys():
                    del self.dict_bombas[pos_valida]
                instancia = self.transformar_casilla(pos_valida, f"X{tipo[1]}")
                self.enviar_mensaje({"mostrar_bomba": [tipo, pos_valida]})
                self.dict_bombas[pos_valida] = instancia

    def adquirir_bomba(self, posicion):
        if posicion in self.dict_items.keys():
            instancia = self.dict_items[posicion]
            tipo = instancia.tipo
            if tipo == "M":
                self.dict_conejochicho[posicion].bomba_m += 1
            elif tipo == "C":
                self.dict_conejochicho[posicion].bomba_c += 1
            self.enviar_mensaje({"eliminar_item": posicion})
            self.enviar_mensaje(
                {"actualizar_menu_inventario": [self.dict_conejochicho[posicion].bomba_m,
                                                self.dict_conejochicho[posicion].bomba_c]})
            self.dict_items[posicion].deleteLater()
            del self.dict_items[posicion]

    def eliminar_bomba(self, posicion):
        self.enviar_mensaje({"eliminar_bomba": posicion})
        self.dict_bombas[posicion].deleteLater()
        del self.dict_bombas[posicion]

    def eliminar_lobo(self, posicion):
        if posicion in self.dict_enemigos.keys() and isinstance(
                self.dict_enemigos[posicion], Lobo):
            self.enviar_mensaje({"eliminar_enemigo": posicion})
            self.dict_enemigos[posicion].deleteLater()
            del self.dict_enemigos[posicion]
            self.lobos_eliminados += 1

    def ralentizar_lobo(self, posicion):
        if posicion in self.dict_enemigos.keys() and isinstance(
                self.dict_enemigos[posicion], Lobo):
            self.senal_ralentizar.emit(posicion)
            self.enviar_mensaje({"ralentizar_enemigo": posicion})

    def terminar(self):
        self.senal_com_casillas.emit({"stop": None})
        self.quit()
        self.wait()
