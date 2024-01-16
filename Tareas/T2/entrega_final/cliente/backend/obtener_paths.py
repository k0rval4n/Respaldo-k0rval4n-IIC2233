import os
from parametros import DICCIONARIO_PATHS_SPRITES
from parametros import PATH_TABLERO_1, PATH_TABLERO_2, PATH_TABLERO_3


def obtener_paths_tableros():
    lista = [PATH_TABLERO_1, PATH_TABLERO_2, PATH_TABLERO_3]
    lista_paths = []
    for nombre_archivo in lista:
        lista_paths.append(os.path.join("assets", "laberintos", nombre_archivo))
    return lista_paths


def obtener_paths_sprites(tipo):
    if tipo in ["-", "E", "S"]:
        tipo = "-"
    lista = DICCIONARIO_PATHS_SPRITES[tipo]
    lista_paths = []
    for nombre_archivo in lista:
        lista_paths.append(os.path.join("assets", "sprites", nombre_archivo))
    return lista_paths
