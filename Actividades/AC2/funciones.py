from copy import copy
from collections import defaultdict
from functools import reduce
from itertools import product
from typing import Generator

from parametros import RUTA_PELICULAS, RUTA_GENEROS
from utilidades import (
    Pelicula, Genero, obtener_unicos, imprimir_peliculas,
    imprimir_generos, imprimir_peliculas_genero
)


# ----------------------------------------------------------------------------
# Parte 1: Cargar dataset
# ----------------------------------------------------------------------------

def cargar_peliculas(ruta: str) -> Generator:
    peliculas = open(ruta, "r")
    lista = peliculas.readlines()
    for pelicula in lista[1:]:
        pelicula = pelicula.strip()
        pelicula = pelicula.split(",")
        yield Pelicula(int(pelicula[0]), pelicula[1], pelicula[2],
                       int(pelicula[3]), float(pelicula[4]))


def cargar_generos(ruta: str) -> Generator:
    generos = open(ruta, "r")
    lista = generos.readlines()
    for genero in lista[1:]:
        genero = genero.strip()
        genero = genero.split(",")
        yield Genero(genero[0], int(genero[1]))


# ----------------------------------------------------------------------------
# Parte 2: Consultas sobre generadores
# ----------------------------------------------------------------------------

def obtener_directores(generador_peliculas: Generator) -> set:
    generador_directores = map(lambda pelicula: pelicula.director,
                               generador_peliculas)
    directores_set = obtener_unicos(generador_directores)
    return directores_set


def obtener_str_titulos(generador_peliculas: Generator) -> str:
    str_titulos = ""
    for pelicula in generador_peliculas:
        str_titulos += (", " + pelicula[1])
    str_titulos = str_titulos.strip(", ")
    return str_titulos


def filtrar_peliculas(
    generador_peliculas: Generator,
    director: str | None = None,
    rating_min: float | None = None,
    rating_max: float | None = None
) -> filter:
    filtrado = generador_peliculas
    if director is not None:
        filtrado = filter(lambda pelicula: director == pelicula.director,
                          filtrado)
    if rating_min is not None:
        filtrado = filter(lambda pelicula: pelicula.rating >= rating_min,
                          filtrado)
    if rating_max is not None:
        filtrado = filter(lambda pelicula: pelicula.rating <= rating_max,
                          filtrado)
    return filtrado


def filtrar_peliculas_por_genero(
    generador_peliculas: Generator,
    generador_generos: Generator,
    genero: str | None = None
) -> Generator:
    producto_cartesiano = product(generador_peliculas, generador_generos)
    if genero is not None:
        return filter(lambda tupla: tupla[1].genero == genero and
                      tupla[0].id_pelicula == tupla[1].id_pelicula,
                      producto_cartesiano)
    else:
        return filter(lambda tupla: tupla[0].id_pelicula ==
                      tupla[1].id_pelicula, producto_cartesiano)


# ----------------------------------------------------------------------------
# Parte 3: Iterables
# ----------------------------------------------------------------------------

class DCCMax:
    def __init__(self, peliculas: list) -> None:
        self.peliculas = peliculas

    def __iter__(self):
        return IteradorDCCMax(self.peliculas)


class IteradorDCCMax:
    def __init__(self, iterable_peliculas: list) -> None:
        self.peliculas = copy(iterable_peliculas)
        self.peliculas.sort(key=lambda pelicula: (pelicula.estreno,
                                                  (-1) * (pelicula.rating)))

    def __iter__(self):
        return self

    def __next__(self) -> tuple:
        if len(self.peliculas) < 1:
            # Se levanta la excepción correspondiente
            raise StopIteration()
        else:
            instancia_pelicula = self.peliculas.pop(0)
            return instancia_pelicula


if __name__ == '__main__':
    print('> Cargar películas:')
    imprimir_peliculas(cargar_peliculas(RUTA_PELICULAS))
    print()

    print('> Cargar géneros')
    imprimir_generos(cargar_generos(RUTA_GENEROS), 5)
    print()

    print('> Obtener directores:')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    print(list(obtener_directores(generador_peliculas)))
    print()

    print('> Obtener string títulos')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    print(obtener_str_titulos(generador_peliculas))
    print()

    print('> Filtrar películas (por director):')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    imprimir_peliculas(filtrar_peliculas(
        generador_peliculas, director='Christopher Nolan'
    ))
    print('\n> Filtrar películas (rating min):')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    imprimir_peliculas(filtrar_peliculas(generador_peliculas, rating_min=9.1))
    print('\n> Filtrar películas (rating max):')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    imprimir_peliculas(filtrar_peliculas(generador_peliculas, rating_max=8.7))
    print()

    print('> Filtrar películas por género')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    generador_generos = cargar_generos(RUTA_GENEROS)
    imprimir_peliculas_genero(filtrar_peliculas_por_genero(
        generador_peliculas, generador_generos, 'Biography'
    ))
    print()

    print('> DCC Max')
    for (estreno, pelis) in DCCMax(list(cargar_peliculas(RUTA_PELICULAS))):
        print(f'\n{estreno:^80}\n')
        imprimir_peliculas(pelis)
