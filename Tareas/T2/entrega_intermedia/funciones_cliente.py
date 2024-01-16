from utilidades_cliente import (riesgo_derecha, riesgo_izquierda,
                                riesgo_abajo, riesgo_arriba)
from copy import deepcopy


def validacion_formato(nombre: str) -> bool:  # NICE
    es_alphaum = nombre.isalnum()
    largo_valido = 3 <= len(nombre) <= 16
    tiene_num = False
    tiene_mayus = False
    for caracter in nombre:
        if caracter.isupper():
            tiene_mayus = True
        if caracter.isnumeric():
            tiene_num = True
    valido = es_alphaum and largo_valido and tiene_num and tiene_mayus
    return valido


def riesgo_mortal(laberinto: list[list]) -> bool:  # NICE
    sigla_entidades_mortales = ["LH", "LV", "CU", "CD", "CL", "CR"]
    lista_entidades_mortales = []
    for fil in range(len(laberinto)):
        for col in range(len(laberinto[fil])):
            if laberinto[fil][col] in sigla_entidades_mortales:
                lista_entidades_mortales.append([laberinto[fil][col],
                                                 (fil, col)])
            elif laberinto[fil][col] == "C":
                coord_conejochico = (fil, col)
    puede_morir = False
    for entidad_mortal in lista_entidades_mortales:
        coords = (entidad_mortal[1][0], entidad_mortal[1][1])
        if (entidad_mortal[0] == sigla_entidades_mortales[0] and
                (riesgo_derecha(coords, laberinto) or
                 riesgo_izquierda(coords, laberinto))):
            puede_morir = True
        elif (entidad_mortal[0] == sigla_entidades_mortales[1] and
                (riesgo_abajo(coords, laberinto) or
                 riesgo_arriba(coords, laberinto))):
            puede_morir = True
        elif (entidad_mortal[0] == sigla_entidades_mortales[2] and
                riesgo_arriba(coords, laberinto)):
            puede_morir = True
        elif (entidad_mortal[0] == sigla_entidades_mortales[3] and
                riesgo_abajo(coords, laberinto)):
            puede_morir = True
        elif (entidad_mortal[0] == sigla_entidades_mortales[4] and
                riesgo_izquierda(coords, laberinto)):
            puede_morir = True
        elif (entidad_mortal[0] == sigla_entidades_mortales[5] and
                riesgo_derecha(coords, laberinto)):
            puede_morir = True

    return puede_morir


def usar_item(item: str, inventario: list) -> tuple[bool, list]:  # NICE
    existe = item in inventario
    inventario_modificado = deepcopy(inventario)
    if not existe:
        return (False, inventario_modificado)
    elif existe:
        inventario_modificado.remove(item)
        return (True, inventario_modificado)


def calcular_puntaje(tiempo: int, vidas: int, cantidad_lobos: int,
                     PUNTAJE_LOBO: int) -> float:  # NICE
    if cantidad_lobos > 0:
        puntaje = (tiempo * vidas) / (cantidad_lobos * PUNTAJE_LOBO)
    elif cantidad_lobos == 0:
        puntaje = float(0)
    return round(puntaje, 2)


def validar_direccion(laberinto: list[list], tecla: str) -> bool:  # NICE
    for fil in range(len(laberinto)):
        for col in range(len(laberinto[fil])):
            if laberinto[fil][col] == "C":
                fil_c = fil
                col_c = col
    mov_valido = False
    c_invalidas = ["P", "CU", "CD", "CL", "CR"]
    if tecla == "W" and laberinto[fil_c - 1][col_c] not in c_invalidas:
        mov_valido = True
    elif tecla == "S" and laberinto[fil_c + 1][col_c] not in c_invalidas:
        mov_valido = True
    elif tecla == "D" and laberinto[fil_c][col_c + 1] not in c_invalidas:
        mov_valido = True
    elif tecla == "A" and laberinto[fil_c][col_c - 1] not in c_invalidas:
        mov_valido = True
    return mov_valido
