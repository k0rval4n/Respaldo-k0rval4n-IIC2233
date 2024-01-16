from typing import List
from clases import Tortuga
import pickle


###################
#### ENCRIPTAR ####
###################
def serializar_tortuga(tortuga: Tortuga) -> bytearray:
    try:
        tortuga_serializada = pickle.dumps(tortuga)
        return bytearray(tortuga_serializada)
    except AttributeError:
        raise ValueError()


def verificar_rango(mensaje: bytearray, inicio: int, fin: int) -> None:
    condicion1 = not inicio < 0 and not fin >= len(mensaje)
    condicion2 = inicio <= fin
    if condicion1 and condicion2:
        return None
    else:
        raise AttributeError()


def codificar_rango(inicio: int, fin: int) -> bytearray:
    bytes_inicio = (inicio).to_bytes(length=3, byteorder="big")
    bytes_fin = (fin).to_bytes(length=3, byteorder="big")
    bytearray_final = bytearray(bytes_inicio)
    bytearray_final.extend(bytes_fin)
    return bytearray_final


def codificar_largo(largo: int) -> bytearray:
    bytes_largo = (largo).to_bytes(length=3, byteorder="big")
    return bytearray(bytes_largo)


def separar_msg(mensaje: bytearray, inicio: int, fin: int) -> List[bytearray]:
    m_extraido = bytearray()
    m_con_mascara = bytearray()
    m_extraido = mensaje[inicio:fin + 1]
    if len(m_extraido) % 2 != 0:
        m_extraido = m_extraido[::-1]
    m_con_mascara = mensaje[:]
    for i in range(inicio, fin + 1):
        m_con_mascara[i] = i - inicio
    return [m_extraido, m_con_mascara]


def encriptar(mensaje: bytearray, inicio: int, fin: int) -> bytearray:
    # Se la damos listas
    verificar_rango(mensaje, inicio, fin)

    m_extraido, m_con_mascara = separar_msg(mensaje, inicio, fin)
    rango_codificado = codificar_rango(inicio, fin)
    return (
        codificar_largo(fin - inicio + 1)
        + m_extraido
        + m_con_mascara
        + rango_codificado
    )


######################
#### DESENCRIPTAR ####
######################
def deserializar_tortuga(mensaje_codificado: bytearray) -> Tortuga:
    try:
        tortuga = pickle.loads(mensaje_codificado)
        return tortuga
    except ValueError:
        raise AttributeError()


def decodificar_largo(mensaje: bytearray) -> int:
    primeros_3bytes = mensaje[0:3]
    return int.from_bytes(primeros_3bytes, byteorder="big")


def separar_msg_encriptado(mensaje: bytearray) -> List[bytearray]:
    m_extraido = bytearray()
    m_con_mascara = bytearray()
    rango_codificado = bytearray()
    largo = decodificar_largo(mensaje)
    m_extraido = mensaje[3:(3 + largo)]
    m_con_mascara = mensaje[(3 + largo):-6]
    rango_codificado = mensaje[-6:]
    if largo % 2 != 0:
        m_extraido = m_extraido[::-1]
    return [m_extraido, m_con_mascara, rango_codificado]


def decodificar_rango(rango_codificado: bytearray) -> List[int]:
    inicio = int.from_bytes(rango_codificado[:3], byteorder="big")
    fin = int.from_bytes(rango_codificado[3:], byteorder="big")
    return [inicio, fin]


def desencriptar(mensaje: bytearray) -> bytearray:
    m_extraido, m_con_mascara, rango_codificado = separar_msg_encriptado(mensaje)
    inicio, fin = decodificar_rango(rango_codificado)
    m_inicio = m_con_mascara[:inicio]
    m_fin = m_con_mascara[(fin + 1):]
    return m_inicio + m_extraido + m_fin


if __name__ == "__main__":
    # Tortuga
    tama = Tortuga("Tama2")
    print("Nombre: ", tama.nombre)
    print("Edad: ", tama.edad)
    print(tama.celebrar_anivesario())
    print()

    # Encriptar
    original = serializar_tortuga(tama)
    print("Original: ", original)
    encriptado = encriptar(original, 6, 24)
    print("Encriptado: ", encriptado)
    print()

    # Desencriptar
    mensaje =  bytearray(b'\x00\x00\x13roT\x07\x8c\x94sesalc\x06\x8c\x00\x00\x00\x00\x00\x80\x04\x958\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12tuga\x94\x93\x94)\x81\x94}\x94(\x8c\x06nombre\x94\x8c\x05Tama2\x94\x8c\x04edad\x94K\x01ub.\x00\x00\x06\x00\x00\x18')
    desencriptado = desencriptar(mensaje)
    tama = deserializar_tortuga(desencriptado)

    # Tortuga
    print("Tortuga: ", tama)
    print("Nombre: ", tama.nombre)
    print("Edad: ", tama.edad)
