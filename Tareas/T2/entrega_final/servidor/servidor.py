import socket
from PyQt6.QtCore import QThread, pyqtSignal, QMutex
import pickle
import os
import json


class Servidor(QThread):
    def __init__(self, port):
        super().__init__()
        self.lock_manejar_mensaje = QMutex()
        self.chunk_size = 36
        self.host = self.definir_host()
        self.usuarios_bloqueados = self.obtener_usuarios_bloqueados()  # set
        self.port = int(port)
        self.sockets_clientes = {}
        self.nombres_clientes = {}
        self.socket_servidor = socket.socket(socket.AF_INET,
                                             socket.SOCK_STREAM)
        self.bind_listen()
        self.start()

    def run(self):
        print(f"| {'Nombre': ^20.20}|{'Tipo': ^28.28}|{'Contenido': ^56.56} |")
        self.aceptar_conexiones_thread()

    def bind_listen(self):
        self.socket_servidor.bind((self.host, self.port))
        self.socket_servidor.listen()

    def aceptar_conexiones_thread(self):
        while True:
            socket_cliente, address = self.socket_servidor.accept()
            self.sockets_clientes[socket_cliente] = address
            listening_client_thread = Listen_client_thread(socket_cliente)
            listening_client_thread.senal_a_servidor.connect(self.manejar_mensaje)
            self.enviar_mensaje({"salon_de_la_fama": self.salon_fama()},
                                socket_cliente)
            listening_client_thread.start()

    def manejar_mensaje(self, mensaje: dict, socket_cliente: socket.socket):
        # print(f"servidor manejando: {mensaje}")
        self.lock_manejar_mensaje.lock()
        keys = mensaje.keys()
        if "intentar_empezar_partida" in keys:
            nombre_usuario = mensaje["intentar_empezar_partida"]
            if nombre_usuario not in self.usuarios_bloqueados:
                nivel = 0
                try:
                    with open(os.path.join("puntaje.txt"), "r") as file:
                        puntaje = file.readlines()
                        lineas = [line.strip().split(",") for line in puntaje]
                        for linea in lineas:
                            if nombre_usuario == linea[0]:
                                nivel = int(linea[1])
                                break
                except FileNotFoundError:
                    with open(os.path.join("puntaje.txt"), "tx") as file:
                        nivel = 0
                self.nombres_clientes[socket_cliente] = nombre_usuario
                self.imprimir_logs({"Conectarse": "-"}, socket_cliente)
                self.enviar_mensaje({"empezar_partida":
                                     [nivel, nombre_usuario]}, socket_cliente)
            else:
                self.enviar_mensaje({"usuario_bloqueado": nombre_usuario}, socket_cliente)
        elif "desconexion" in keys:
            if socket_cliente in self.nombres_clientes.keys():
                self.imprimir_logs({"Desconexion": "-"}, socket_cliente)
                del self.nombres_clientes[socket_cliente]
            if socket_cliente in self.sockets_clientes.keys():
                del self.sockets_clientes[socket_cliente]
        elif "pasar_nivel" in keys:
            lista = list(mensaje.values())[0]
            nombre_usuario = lista[0]
            n_nivel_completado = int(lista[1])
            puntaje = float(lista[2])
            ya_existe = False
            try:
                with open(os.path.join("puntaje.txt"), "r") as file:
                    lineas = []
                    puntaje_archivo = file.readlines()
                    for line in puntaje_archivo:
                        linea = line.strip().split(",")
                        lineas.append([linea[0], int(linea[1]), float(linea[2])])
                    for indice in range(len(lineas)):
                        linea = lineas[indice]
                        if linea[0] == nombre_usuario and ya_existe is False:
                            ya_existe = True
                            lineas[indice][1] = str(n_nivel_completado)
                            puntaje_acumulado = linea[2] + puntaje
                            lineas[indice][2] = str(puntaje_acumulado)
                        else:
                            lineas[indice][1] = str(lineas[indice][1])
                            lineas[indice][2] = str(lineas[indice][2])
                        lineas[indice] = ",".join(lineas[indice])
                        lineas[indice] += "\n"
                    if not ya_existe:
                        lineas.append(f"{nombre_usuario},{n_nivel_completado},{puntaje}\n")
                        puntaje_acumulado = puntaje
                    lineas.sort(key=(lambda line: line[2]), reverse=True)
            except FileNotFoundError:
                with open(os.path.join("puntaje.txt"), "tx") as file:
                    file.write(f"{nombre_usuario},{n_nivel_completado},{puntaje}\n")
            with open(os.path.join("puntaje.txt"), "w") as file:
                file.writelines(lineas)
            self.imprimir_logs({"Pasar nivel": f"Puntaje: {puntaje}"},
                               socket_cliente)
        elif "game_win" in keys:
            lista = list(mensaje.values())[0]
            nombre_usuario = lista[0]
            n_nivel_completado = int(lista[1])
            puntaje = float(lista[2])
            ya_existe = False
            try:
                with open(os.path.join("puntaje.txt"), "r") as file:
                    lineas = []
                    puntaje_archivo = file.readlines()
                    for line in puntaje_archivo:
                        linea = line.strip().split(",")
                        lineas.append([linea[0], int(linea[1]), float(linea[2])])
                    for indice in range(len(lineas)):
                        linea = lineas[indice]
                        if linea[0] == nombre_usuario and ya_existe is False:
                            ya_existe = True
                            lineas[indice][1] = str(n_nivel_completado)
                            puntaje_acumulado = linea[2] + puntaje
                            lineas[indice][2] = str(puntaje_acumulado)
                        else:
                            lineas[indice][1] = str(lineas[indice][1])
                            lineas[indice][2] = str(lineas[indice][2])
                        lineas[indice] = ",".join(lineas[indice])
                        lineas[indice] += "\n"
                    if not ya_existe:
                        lineas.append(f"{nombre_usuario},{n_nivel_completado},{puntaje}\n")
                        puntaje_acumulado = puntaje
                    lineas.sort(key=(lambda line: line[2]), reverse=True)
            except FileNotFoundError:
                with open(os.path.join("puntaje.txt"), "tx") as file:
                    file.write(f"{nombre_usuario},{n_nivel_completado},{puntaje}\n")
            with open(os.path.join("puntaje.txt"), "w") as file:
                file.writelines(lineas)
            self.imprimir_logs(
                {"Termino de partida": f"Puntaje acumulado: {puntaje_acumulado}"}, socket_cliente)
        self.lock_manejar_mensaje.unlock()

    def enviar_mensaje(self, mensaje, socket_cliente: socket.socket):
        byte_array = self.serializar_mensaje(mensaje)
        byte_array_encriptado = self.encriptar_mensaje(byte_array)
        lista_codificada = self.codificar_mensaje(byte_array_encriptado)
        # largo, n_bloque, chunk, n_bloque, chunk, ...
        # self.imprimir_logs(mensaje, socket_cliente)
        for byte_array in lista_codificada:
            socket_cliente.sendall(bytes(byte_array))

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

    def definir_host(self):
        with open(os.path.join("parametros_servidor.JSON"), "r") as file:
            json_cargado = json.load(file)
            file.close()
            return json_cargado["host"]

    def imprimir_logs(self, mensaje: dict, socket_cliente: socket.socket):
        col1 = self.nombres_clientes[socket_cliente]  # Nombre de usuario
        col2, col3 = list(zip(mensaje.keys(), mensaje.values()))[0]  # Tipo, Contenido
        largo = max(len(col1), len(col2), len(col3))
        col1 += " " * (largo - len(col1))
        col2 += " " * (largo - len(col2))
        col3 += " " * (largo - len(col3))
        n = 55
        lista = [(col1[i:i+n], col2[i:i+n], col3[i:i+n])
                 for i in range(0, largo, n)]
        for fila in lista:
            c1 = f"{fila[0].strip(): ^19.19}"
            c2 = f"{fila[1].strip(): ^26.26}"
            c3 = f"{fila[2].strip(): ^55.55}"
            print(f"| {c1} | {c2} | {c3} |")
        """esp = '-' * 56
        print(f"| {esp: ^20.20}|{esp: ^28.28}|{esp: ^56.56} |")"""

    def salon_fama(self):
        try:
            with open(os.path.join("puntaje.txt"), "r") as file:
                puntaje = file.readlines()
                lineas = [line.strip().split(",") for line in puntaje]
                lineas = [[line[0], float(line[2])] for line in lineas]
                # 0 = nombre, 1 = nivel, 2 = puntaje
                lineas.sort(key=(lambda line: line[1]), reverse=True)
                mejores_5 = [lineas[i] for i in range(min(5, len(lineas)))]
                return mejores_5
        except FileNotFoundError:
            with open(os.path.join("puntaje.txt"), "tx") as file:
                return ["-", 0]

    def obtener_usuarios_bloqueados(self):
        try:
            with open(os.path.join("usuarios_bloqueados.txt"), "r") as file:
                bloqueados = file.readlines()
                usu_bloq = set()
                [usu_bloq.add(usu.strip()) for usu in bloqueados]
                return usu_bloq
        except FileNotFoundError:
            with open(os.path.join("usuarios_bloqueados.txt"), "tx") as file:
                return set()


class Listen_client_thread(QThread):
    senal_a_servidor = pyqtSignal(dict, socket.socket)

    def __init__(self, socket_cliente: socket.socket):
        super().__init__()
        self.socket_cliente = socket_cliente
        self.chunk_size = 36

    def run(self) -> None:
        while True:
            largo_bytes = self.recibir_bytes(self.socket_cliente, 4)
            largo_mensaje = int.from_bytes(largo_bytes, 'big')
            if largo_mensaje == 0:
                self.senal_a_servidor.emit({"desconexion": None},
                                           self.socket_cliente)
                self.quit()
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
                self.senal_a_servidor.emit(mensaje, self.socket_cliente)
            except ConnectionError:
                self.senal_a_servidor.emit({"desconexion": None},
                                           self.socket_cliente)
                self.quit()
                break
            except OSError:
                self.senal_a_servidor.emit({"desconexion": None},
                                           self.socket_cliente)
                self.quit()
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
