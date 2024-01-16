def usuario_permitido(nombre: str, usuarios_no_permitidos: list[str]) -> bool:
    es_valido = nombre not in usuarios_no_permitidos
    return es_valido


def serializar_mensaje(mensaje: str) -> bytearray:
    bytes = mensaje.encode(encoding="utf-8")
    byte_array = bytearray(bytes)
    return byte_array


def separar_mensaje(mensaje: bytearray) -> list[bytearray]:
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


def encriptar_mensaje(mensaje: bytearray) -> bytearray:
    lista_bytearrays = separar_mensaje(mensaje)
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


def codificar_mensaje(mensaje: bytearray) -> list[bytearray]:
    lista_codificada = []
    largo = len(mensaje)
    bytearray_largo = bytearray(largo.to_bytes(4, byteorder="big"))
    lista_codificada.append(bytearray_largo)
    while len(mensaje) % 36 != 0:
        mensaje.extend(b"\x00")
    for inicio in range(0, largo, 36):
        fin = inicio + 36
        n_bloque = int(inicio / 36) + 1
        bytearray_n_bloque = bytearray(n_bloque.to_bytes(4, byteorder="big"))
        lista_codificada.append(bytearray_n_bloque)
        byte_data = mensaje[inicio:fin]
        lista_codificada.append(byte_data)
    return lista_codificada
