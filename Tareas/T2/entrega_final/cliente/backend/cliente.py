import socket
import os
import json
import pickle
from PyQt6.QtCore import pyqtSignal, QThread
from backend.partida import Partida
from parametros import DICT_PARAMETROS_INICIALES


class Cliente(QThread):
    senal_a_ventana = pyqtSignal(dict)
    senal_a_partida = pyqtSignal(dict)

    def __init__(self, port_servidor) -> None:
        super().__init__()
        self.puntaje_partida = 0
        self.conectado = False
        self.port_servidor = port_servidor
        self.host_servidor = self.definir_host()
        self.chunk_size = 36
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket_cliente.connect((self.host_servidor,
                                         self.port_servidor))
            self.conectado = True
        except ConnectionError:
            self.socket_cliente.close()
            self.conectado = False
            self.senal_a_ventana.emit({"error_de_conexion": "init"})
        else:
            self.start()

    def run(self):
        self.listening_server_thread = Listen_server_thread(self.socket_cliente)
        self.listening_server_thread.senal_a_cliente.connect(self.manejar_mensaje)
        self.listening_server_thread.start()

    def manejar_mensaje(self, mensaje: dict):
        keys = mensaje.keys()
        if "game_over" in keys:
            self.senal_a_partida.emit({"boton_pausa": None})
            self.senal_a_partida.emit({"boton_salir": None})
            self.senal_a_ventana.emit({"game_over": [self.nombre_usuario, self.puntaje_partida]})
            self.conectado = False
            self.enviar_mensaje({"desconexion": None})
            self.quit()
            self.wait()
        elif "desconexion" in keys:
            self.senal_a_partida.emit({"boton_pausa": None})
            self.senal_a_partida.emit({"boton_salir": None})
            self.senal_a_ventana.emit({"error_de_conexion": "init"})

        elif "intentar_empezar_partida" in keys:
            self.enviar_mensaje(mensaje)
        elif "empezar_partida" in keys:
            nivel, nombre = mensaje["empezar_partida"]
            self.nombre_usuario = nombre
            self.partida = Partida(nivel + 1)
            self.partida.senal_a_cliente.connect(self.manejar_mensaje)
            self.senal_a_partida.connect(self.partida.manejar_mensaje)
            self.partida.start()
            self.senal_a_partida.emit(
                {"empezar_partida": [nivel + 1, nombre, DICT_PARAMETROS_INICIALES]})
        elif "usuario_bloqueado" in keys:
            self.senal_a_ventana.emit(mensaje)
        elif "dict_inicial" in keys:
            self.senal_a_ventana.emit(mensaje)
        elif "pasar_nivel" in keys:
            self.puntaje_partida += mensaje["pasar_nivel"][2]
            self.enviar_mensaje(mensaje)
            self.senal_a_ventana.emit(mensaje)
        elif "game_win" in keys:
            self.puntaje_partida += mensaje["game_win"][2]
            self.senal_a_partida.emit({"boton_pausa": None})
            self.senal_a_partida.emit({"boton_salir": None})
            self.senal_a_ventana.emit({"game_win": [self.nombre_usuario, self.puntaje_partida]})
            self.enviar_mensaje(mensaje)
            self.quit()
            self.wait()
        elif "salon_de_la_fama" in keys:
            self.msg_fama = mensaje
            self.senal_a_ventana.emit(mensaje)
        elif "boton_salir" in keys:
            self.senal_a_partida.emit(mensaje)
            self.quit()
            self.wait()
        elif "boton_salir_b" in keys:
            self.senal_a_partida.emit({"boton_salir": None})
        elif "boton_salir_ventanajuego" in keys:
            self.senal_a_partida.emit({"boton_salir": None})
            self.enviar_mensaje({"desconexion": None})
        elif "boton_pausa" in keys:
            self.senal_a_partida.emit(mensaje)
        elif "cargado" in keys:
            self.senal_a_partida.emit(mensaje)
        elif "mover_jugador" in keys or "mostrar_bomba" in keys or \
                "eliminar_bomba" in keys or "mover_enemigo" in keys or \
                "anadir_enemigo" in keys or "eliminar_enemigo" in keys:
            self.senal_a_ventana.emit(mensaje)
        elif "intentar_mover_jugador" in keys:
            self.senal_a_partida.emit(mensaje)
        elif "TIEMPO_ACTUAL" in keys:
            self.senal_a_ventana.emit(mensaje)
        elif "parametros_tablero" in keys:
            self.senal_a_ventana.emit(mensaje)
        elif "muerte" in keys or "pasar_nivel" in keys:
            self.senal_a_ventana.emit(mensaje)
        elif "intentar_usar_bomba" in keys:
            self.senal_a_partida.emit(mensaje)
        elif "jugador_movido" in keys:
            self.senal_a_ventana.emit(mensaje)
        elif "tiempo_agotado" in keys:
            self.senal_a_ventana.emit(mensaje)
        elif "eliminar_item" in keys:
            self.senal_a_ventana.emit(mensaje)
        elif "intentar_adquirir_bomba" in keys:
            self.senal_a_partida.emit(mensaje)
        elif "actualizar_menu_inventario" in keys:
            self.senal_a_ventana.emit(mensaje)
        elif "dame_salon_fama" in keys:
            self.senal_a_ventana.emit(self.msg_fama)
        elif "ralentizar_enemigo" in keys:
            self.senal_a_ventana.emit(mensaje)
        elif "cheat_inf" in keys or "cheat_kil" in keys:
            self.senal_a_partida.emit(mensaje)

    def definir_host(self):
        with open(os.path.join("parametros_cliente.JSON"), "r") as file:
            json_cargado = json.load(file)
            file.close()
            return json_cargado["host_servidor"]

    def recibir_bytes(self, socket_cliente, cantidad):
        bytes_recibidos = bytearray()
        while len(bytes_recibidos) < cantidad:
            cantidad_restante = cantidad - len(bytes_recibidos)
            bytes_leer = min(self.chunk_size, cantidad_restante)
            respuesta = socket_cliente.recv(bytes_leer)
            """if len(respuesta) < bytes_leer:
                return bytes_recibidos"""
            bytes_recibidos += respuesta
        return bytes_recibidos

    def enviar_mensaje(self, mensaje: dict):
        byte_array = self.serializar_mensaje(mensaje)
        byte_array_encriptado = self.encriptar_mensaje(byte_array)
        lista_codificada = self.codificar_mensaje(byte_array_encriptado)
        # largo, n_bloque, chunk, n_bloque, chunk, ...
        for byte_array in lista_codificada:
            try:
                self.socket_cliente.sendall(bytes(byte_array))
            except ConnectionError:
                self.conectado = False
                self.senal_a_ventana.emit({"error_de_conexion": None})
                self.quit()
                self.wait()
                break
            except OSError:
                self.conectado = False
                self.senal_a_ventana.emit({"error_de_conexion": None})
                self.quit()
                self.wait()
                break

    def serializar_mensaje(self, mensaje) -> bytearray:
        bytes = pickle.dumps(mensaje)
        byte_array = bytearray(bytes)
        return byte_array

    def separar_mensaje(self, mensaje: bytearray) -> list[bytearray]:
        a = bytearray()
        b = bytearray()
        c = bytearray()
        lista_bytearrays = [a, b, c]
        contador = 0
        while contador < len(mensaje):
            for i in range(3):
                if contador < len(mensaje):
                    lista_bytearrays[i].extend(mensaje[contador:contador + 1])
                    contador += 1
            for i in range(2, -1, -1):
                if contador < len(mensaje):
                    lista_bytearrays[i].extend(mensaje[contador:contador + 1])
                    contador += 1
        return lista_bytearrays

    def encriptar_mensaje(self, mensaje: bytearray) -> bytearray:
        lista_bytearrays = self.separar_mensaje(mensaje)
        a, b, c = lista_bytearrays[0], lista_bytearrays[1], lista_bytearrays[2]
        suma_int = (int.from_bytes(a[0:1], byteorder="big") +
                    int.from_bytes(b[-1:], byteorder="big") +
                    int.from_bytes(c[0:1], byteorder="big"))
        if suma_int % 2 == 0:
            acb = a + c + b
            return bytearray(b"1") + acb
        else:
            bac = b + a + c
            return bytearray(b"0") + bac

    def codificar_mensaje(self, mensaje: bytearray) -> list[bytearray]:
        lista_codificada = []
        largo = len(mensaje)
        bytearray_largo = bytearray(largo.to_bytes(4, byteorder="big"))
        lista_codificada.append(bytearray_largo)
        while len(mensaje) % 36 != 0:
            mensaje.extend(b"\x00")
        for inicio in range(0, largo, 36):
            fin = inicio + 36
            n_bloque = int(inicio / 36) + 1
            bytearray_n_bloque = bytearray(n_bloque.to_bytes(4,
                                                             byteorder="big"))
            lista_codificada.append(bytearray_n_bloque)
            byte_data = mensaje[inicio:fin]
            lista_codificada.append(byte_data)
        return lista_codificada


class Listen_server_thread(QThread):
    senal_a_cliente = pyqtSignal(dict, socket.socket)

    def __init__(self, socket_cliente: socket.socket):
        super().__init__()
        self.socket_cliente = socket_cliente
        self.chunk_size = 36

    def run(self) -> None:
        while True:
            largo_bytes = self.recibir_bytes(self.socket_cliente, 4)
            largo_mensaje = int.from_bytes(largo_bytes, 'big')
            if largo_mensaje == 0:
                self.senal_a_cliente.emit({"desconexion": None}, self.socket_cliente)
                break
            lista_codificada = []
            lista_codificada.append(largo_bytes)
            for inicio in range(0, largo_mensaje, self.chunk_size):
                n_chunk = self.recibir_bytes(self.socket_cliente, 4)
                bytes_recibidos = self.recibir_bytes(self.socket_cliente,
                                                     self.chunk_size)
                lista_codificada.append(n_chunk)
                lista_codificada.append(bytes_recibidos)
            try:
                mensaje = self.traducir_bytes(lista_codificada)
                self.senal_a_cliente.emit(mensaje, self.socket_cliente)
            except ConnectionError:
                self.conectado = False
                self.senal_a_cliente.emit({"desconexion": None}, self.socket_cliente)
                break
            except OSError:
                self.conectado = False
                self.senal_a_cliente.emit({"desconexion": None}, self.socket_cliente)
                break

    def recibir_bytes(self, socket_cliente, cantidad):
        bytes_recibidos = bytearray()
        while len(bytes_recibidos) < cantidad:
            cantidad_restante = cantidad - len(bytes_recibidos)
            bytes_leer = min(self.chunk_size, cantidad_restante)
            respuesta = socket_cliente.recv(bytes_leer)
            if len(respuesta) < bytes_leer:
                return bytes_recibidos
            bytes_recibidos += respuesta
        return bytes_recibidos

    def decodificar_bytes(self, lista_codificada):
        largo_mensaje = int.from_bytes(lista_codificada[0], byteorder="big")
        lista_decodificada = []
        lista_decodificada.append(largo_mensaje)
        for inicio in range(1, len(lista_codificada), 2):
            n_chunk = lista_codificada[inicio]
            bytes_recibidos = lista_codificada[inicio + 1]
            lista_decodificada.append([n_chunk, bytes_recibidos])
        return lista_decodificada

    def desencriptar(self, lista_decodificada):
        n = lista_decodificada[1][1][0:1]  # [0 = nBAC] o [1 = nACB]
        largo_mensaje = lista_decodificada[0]
        largo_data = largo_mensaje - 1
        byte_array_desencriptado = bytearray()
        for fila in lista_decodificada[1:]:
            byte_array_desencriptado += (fila[1])
        lista_a = []
        lista_b = []
        lista_c = []
        lista_abc = [lista_a, lista_b, lista_c]
        contador = 0
        while contador < largo_data:
            for i in range(3):
                if contador < largo_data:
                    lista_abc[i].append(contador)
                    contador += 1
            for i in range(2, -1, -1):
                if contador < largo_data:
                    lista_abc[i].append(contador)
                    contador += 1
        largo_a = len(lista_a)
        largo_b = len(lista_b)
        largo_c = len(lista_c)
        if n == b"0":  # [0 = nBAC]
            b = byte_array_desencriptado[1:largo_b + 1]
            a = byte_array_desencriptado[largo_b + 1:largo_b + largo_a + 1]
            c = byte_array_desencriptado[largo_b + largo_a + 1:largo_b + largo_a + largo_c + 1]
        elif n == b"1":  # [1 = nACB]
            a = byte_array_desencriptado[1:largo_a + 1]
            c = byte_array_desencriptado[largo_a + 1:largo_a + largo_c + 1]
            b = byte_array_desencriptado[largo_a + largo_c + 1:largo_a + largo_c + largo_b + 1]
        byte_array_desencriptado = byte_array_desencriptado[1:largo_mensaje + 1]
        for i in range(len(lista_a)):
            posicion = lista_a[i]
            byte_array_desencriptado[posicion:posicion + 1] = a[i:i + 1]
        for i in range(len(lista_b)):
            posicion = lista_b[i]
            byte_array_desencriptado[posicion:posicion + 1] = b[i:i + 1]
        for i in range(len(lista_c)):
            posicion = lista_c[i]
            byte_array_desencriptado[posicion:posicion + 1] = c[i:i + 1]
        return byte_array_desencriptado

    def deserializar(self, byte_array_desencriptado):
        mensaje = pickle.loads(bytes(byte_array_desencriptado))
        return mensaje

    def traducir_bytes(self, lista_codificada):
        lista_decodificada = self.decodificar_bytes(lista_codificada)
        byte_array_desencriptado = self.desencriptar(lista_decodificada)
        mensaje = self.deserializar(byte_array_desencriptado)
        return mensaje
