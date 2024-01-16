
import collections
import datetime
from functools import reduce
import itertools
import math
import utilidades

from typing import Generator

from utilidades import Personas, Peliculas, Funciones, Reservas


def peliculas_genero(generador_peliculas: Generator, genero: str):
    return filter(lambda pelicula: pelicula.genero == genero, generador_peliculas)


def personas_mayores(generador_personas: Generator, edad: int):
    return filter(lambda persona: persona.edad >= edad, generador_personas)


def funciones_fecha(generador_funciones: Generator, fecha: str):
    fecha = fecha[:6] + fecha[8:]
    return filter(lambda funcion: funcion.fecha == fecha, generador_funciones)


def titulo_mas_largo(generador_peliculas: Generator) -> str:
    def key(pelicula1, pelicula2):
        if len(pelicula1.titulo) > len(pelicula2.titulo):
            return pelicula1
        elif len(pelicula1.titulo) < len(pelicula2.titulo):
            return pelicula2
        else:
            if float(pelicula1.rating) > float(pelicula2.rating):
                return pelicula1
            else:
                return pelicula2
    namedtuple_pelicula = reduce(key, generador_peliculas)
    return namedtuple_pelicula.titulo


def normalizar_fechas(generador_funciones: Generator):
    #  DD-MM-AA -> AAAA-MM-DD
    def key(funcion):
        dia = funcion.fecha[0:2]
        mes = funcion.fecha[3:5]
        ano = funcion.fecha[6:8]
        if int(ano) < 24:
            ano = "20" + ano
        else:
            ano = "19" + ano
        lista = [i for i in funcion]
        lista[4] = ano + "-" + mes + "-" + dia
        return Funciones(*(i for i in lista))
    return map(key, generador_funciones)


def personas_reservas(generador_reservas: Generator):
    return {reserva.id_persona for reserva in generador_reservas}


def peliculas_en_base_al_rating(generador_peliculas: Generator, genero: str, rating_min: int,
                                rating_max: int):
    def key(pelicula):
        if pelicula.genero == genero and rating_min <= float(pelicula.rating) <= rating_max:
            return True
        else:
            return False
    return filter(key, generador_peliculas)
    # return map(lambda pelicula: pelicula.titulo, filtradas)


def mejores_peliculas(generador_peliculas: Generator):
    def criterio(pelicula1, pelicula2):
        if pelicula1.rating > pelicula2.rating:
            return pelicula1
        elif pelicula1.rating == pelicula2.rating:
            if pelicula1.id < pelicula2.id:
                return pelicula1
            else:
                return pelicula2
        else:
            return pelicula2

    def uso_criterio(lista):
        mejor = reduce(criterio, lista, lista[0])
        lista_peliculas.remove(mejor)
        return mejor
    lista_peliculas = [pelicula for pelicula in generador_peliculas]
    if len(lista_peliculas) <= 20:
        return lista_peliculas
    else:
        real = [uso_criterio(lista_peliculas) for i in range(20)]
        return real


def pelicula_genero_mayor_rating(generador_peliculas: Generator, genero: str) -> str:
    peliculas_filtradas = filter(lambda pelicula: pelicula.genero == genero, generador_peliculas)
    lista_filtradas = [pelicula for pelicula in peliculas_filtradas]
    if len(lista_filtradas) > 0:
        return reduce(lambda pelicula1, pelicula2: pelicula1 if float(pelicula1.rating) >=
                      float(pelicula2.rating) else pelicula2, lista_filtradas).titulo
    else:
        return ""


def fechas_funciones_pelicula(generador_peliculas: Generator, generador_funciones: Generator,
                              titulo: str):
    lista_pelicula = [pelicula for pelicula in generador_peliculas if
                      pelicula.titulo == titulo]
    if len(lista_pelicula) > 0:
        id_pelicula = lista_pelicula[0].id
    else:
        id_pelicula = "a"
    funciones_validas = filter(lambda funcion: funcion.id_pelicula == id_pelicula,
                               generador_funciones)
    return map(lambda funcion: funcion.fecha, funciones_validas)


def genero_mas_transmitido(generador_peliculas: Generator, generador_funciones: Generator,
                           fecha: str) -> str:
    fecha = fecha[:6] + fecha[8:]
    dict_pelicula = {pelicula.id: pelicula.genero for pelicula in generador_peliculas}
    funciones_filtradas = filter(lambda funcion: funcion.fecha == fecha, generador_funciones)
    genero_f_filtradas = map(lambda funcion: dict_pelicula[funcion.id_pelicula],
                             funciones_filtradas)
    lista_f_filtradas = [genero for genero in genero_f_filtradas]
    if len(lista_f_filtradas) > 0:
        dict_cantidad = {genero: lista_f_filtradas.count(genero) for genero in lista_f_filtradas}
        mas_trans = reduce(lambda genero1, genero2: genero1 if dict_cantidad[genero1] >=
                           dict_cantidad[genero2] else genero2, dict_cantidad)
        return mas_trans
    else:
        return ""


def id_funciones_genero(generador_peliculas: Generator, generador_funciones: Generator,
                        genero: str):
    peliculas_genero = filter(lambda pelicula: pelicula.genero == genero, generador_peliculas)
    id_peliculas_genero = [pelicula.id for pelicula in peliculas_genero]
    funciones_genero = filter(lambda funcion: funcion.id_pelicula in id_peliculas_genero,
                              generador_funciones)
    return map(lambda funcion: funcion.id, funciones_genero)


def butacas_por_funcion(generador_reservas: Generator, generador_funciones: Generator,
                        id_funcion: int) -> int:
    reservas = filter(lambda reserva: reserva.id_funcion == id_funcion, generador_reservas)
    return reduce(lambda reserva1, reserva2: reserva1 + 1, reservas, 0)


def salas_de_pelicula(generador_peliculas: Generator, generador_funciones: Generator,
                      nombre_pelicula: str):
    lista_id = [pelicula.id for pelicula in generador_peliculas if pelicula.titulo ==
                nombre_pelicula]
    if len(lista_id) > 0:
        id = lista_id[0]
    else:
        id = "a"
    funciones = filter(lambda funcion: funcion.id_pelicula == id, generador_funciones)
    return map(lambda funcion: funcion.numero_sala, funciones)


def nombres_butacas_altas(generador_personas: Generator, generador_peliculas: Generator,
                          generador_reservas: Generator,
                          generador_funciones: Generator, titulo: str, horario: int):
    lista = [i.id for i in generador_peliculas if i.titulo == titulo]
    if len(lista) > 0:
        id_pelicula = lista[0]
    else:
        id_pelicula = "a"
    funciones_horario_id = filter(lambda funcion: (funcion.horario == horario and
                                  funcion.id_pelicula == id_pelicula), generador_funciones)
    id_funciones = map(lambda funcion: funcion.id, funciones_horario_id)
    lista_id_funciones = [id for id in id_funciones]
    reservas = filter(lambda reserv: reserv.id_funcion in lista_id_funciones, generador_reservas)
    id_personas = map(lambda reserva: reserva.id_persona, reservas)
    lista_id_personas = [id for id in id_personas]
    personas_validas = filter(lambda persona: persona.id in lista_id_personas, generador_personas)
    return map(lambda persona: persona.nombre, personas_validas)


def nombres_persona_genero_mayores(generador_personas: Generator, generador_peliculas: Generator,
                                   generador_reservas: Generator, generador_funciones: Generator,
                                   nombre_pelicula: str, genero: str, edad: int):
    lista = [i.id for i in generador_peliculas if i.titulo == nombre_pelicula]
    if len(lista) > 0:
        id_pelicula = lista[0]
    else:
        id_pelicula = "a"
    funciones_filtradas = filter(lambda funcion: funcion.id_pelicula == id_pelicula,
                                 generador_funciones)
    id_funciones = map(lambda funcion: funcion.id, funciones_filtradas)
    lista_id_funciones = [id for id in id_funciones]
    reservas = filter(lambda reserv: reserv.id_funcion in lista_id_funciones, generador_reservas)
    id_personas = map(lambda reserva: reserva.id_persona, reservas)
    lista_id_personas = [id for id in id_personas]
    personas_validas = filter(lambda persona: persona.id in lista_id_personas and
                              persona.genero == genero and persona.edad >= edad,
                              generador_personas)
    return {persona.nombre for persona in personas_validas}


def genero_comun(generador_personas: Generator, generador_peliculas: Generator, generador_reservas:
                 Generator, generador_funciones: Generator, id_funcion: int) -> str:
    lista = [funcion for funcion in generador_funciones if funcion.id == id_funcion]
    if len(lista) > 0:
        id_pelicula = lista[0].id_pelicula
        pel = filter(lambda pelicula: pelicula.id == id_pelicula, generador_peliculas)
        lista_pelicula = [pelicula.titulo for pelicula in pel]
        if len(lista_pelicula) > 0:
            nombre_pelicula = lista_pelicula[0]
        reservas = filter(lambda reserva: reserva.id_funcion == id_funcion, generador_reservas)
        lista_id_personas = [reserva.id_persona for reserva in reservas]
        personas = filter(lambda persona: persona.id in lista_id_personas, generador_personas)
        lista_generos = [persona.genero for persona in personas]
        set_generos = {genero for genero in lista_generos}
        set_a_lista = [genero for genero in set_generos]
        dict_generos = {genero: lista_generos.count(genero) for genero in set_a_lista}
        valor_maximo = dict_generos[max(dict_generos, key=dict_generos.get)]
        ganadores = filter(lambda genero: dict_generos[genero] == valor_maximo, set_a_lista)
        lista_ganadores = [genero for genero in ganadores]
        if len(lista_ganadores) == 1:
            genero = lista_ganadores[0]
            return f"En la función {id_funcion} de la película {nombre_pelicula} " \
                   f"la mayor parte del público es {genero}."
        elif len(lista_ganadores) == 2:
            genero_1 = lista_ganadores[0]
            genero_2 = lista_ganadores[1]
            return f"En la función {id_funcion} de la película {nombre_pelicula} se obtiene que " \
                   f"la mayor parte del público es de {genero_1} y {genero_2} con la misma " \
                   f"cantidad de personas."
        else:
            return f"En la función {id_funcion} de la película {nombre_pelicula} se obtiene que " \
                   f"la cantidad de personas es igual para todos los géneros."


def edad_promedio(generador_personas: Generator, generador_peliculas: Generator,
                  generador_reservas: Generator, generador_funciones: Generator,
                  id_funcion: int) -> str:
    lista = [funcion for funcion in generador_funciones if funcion.id == id_funcion]
    if len(lista) > 0:
        id_pelicula = lista[0].id_pelicula
        pel = filter(lambda pelicula: pelicula.id == id_pelicula, generador_peliculas)
        lista_pelicula = [pelicula.titulo for pelicula in pel]
        if len(lista_pelicula) > 0:
            nombre_pelicula = lista_pelicula[0]
        reservas = filter(lambda reserva: reserva.id_funcion == id_funcion, generador_reservas)
        lista_id_personas = [reserva.id_persona for reserva in reservas]
        personas = filter(lambda persona: persona.id in lista_id_personas, generador_personas)
        lista_edades = [persona.edad for persona in personas]
        suma_edades = reduce(lambda x, y: x + y, lista_edades, 0)
        promedio = suma_edades / len(lista_edades)
        promedio_aprox = math.ceil(promedio)
        return f"En la función {id_funcion} de la película {nombre_pelicula} la edad promedio " \
               f"del público es {promedio_aprox}."
    else:
        return ""


def obtener_horarios_disponibles(generador_peliculas: Generator, generador_reservas: Generator,
                                 generador_funciones: Generator, fecha_funcion: str,
                                 reservas_maximas: int):
    fecha = fecha_funcion
    lista_peliculas = [pelicula for pelicula in generador_peliculas]
    lista_peliculas.sort(key=lambda pelicula: pelicula.rating, reverse=True)
    pelicula_buscada = lista_peliculas[0].id
    funciones_en_fecha = filter(lambda funcion: funcion.fecha == fecha and funcion.id_pelicula ==
                                pelicula_buscada, generador_funciones)
    lista_funciones_en_fecha = [funcion for funcion in funciones_en_fecha]
    lista_id_funciones = [funcion.id for funcion in lista_funciones_en_fecha]
    ####
    reservas = filter(lambda reserva: reserva.id_funcion in lista_id_funciones, generador_reservas)
    lista_reservas_id = [reserva.id_funcion for reserva in reservas]
    dict_butacas_funciones = {id_funcion: lista_reservas_id.count(id_funcion)
                              for id_funcion in lista_id_funciones}
    funciones_disponibles = filter(lambda id_funcion: dict_butacas_funciones[id_funcion] <
                                   reservas_maximas, lista_id_funciones)
    lista_funciones_disponibles = [funcion for funcion in funciones_disponibles]
    func = filter(lambda funcion: funcion.id in lista_funciones_disponibles,
                  lista_funciones_en_fecha)
    return {funcion.horario for funcion in func}


def personas_no_asisten(generador_personas: Generator, generador_reservas: Generator,
                        generador_funciones: Generator, fecha_inicio: str, fecha_termino: str):
    dia_i = int(fecha_inicio[0:2])
    mes_i = int(fecha_inicio[3:5])
    ano_i = int(fecha_inicio[6:10])
    # print(f"ano {ano_i}, mes {mes_i}, dia {dia_i}")
    dia_f = int(fecha_termino[0:2])
    mes_f = int(fecha_termino[3:5])
    ano_f = int(fecha_termino[6:10])
    # print(f"ano {ano_f}, mes {mes_f}, dia {dia_f}")

    def fecha(funcion):
        dia = int(funcion.fecha[0:2])
        mes = int(funcion.fecha[3:5])
        if int(funcion.fecha[6:8]) < 24:
            ano = int("20" + funcion.fecha[6:8])
        else:
            ano = int("19" + funcion.fecha[6:8])
        # print(f"ano {ano}, mes {mes}, dia {dia}")
        if ano_i < ano < ano_f:
            return True
        if ano == ano_i == ano_f:
            if mes_i < mes < mes_f:
                return True
            elif mes == mes_i == mes_f:
                if dia_i <= dia <= dia_f:
                    return True
            elif mes == mes_i:
                if dia_i <= dia:
                    return True
            elif mes == mes_f:
                if dia <= dia_f:
                    return True
        elif ano == ano_i:
            if mes_i < mes:
                return True
            elif mes == mes_i:
                if dia_i <= dia:
                    return True
        elif ano == ano_f:
            if mes < mes_f:
                return True
            elif mes == mes_f:
                if dia <= dia_f:
                    return True
        return False
    funciones_dentro_fecha = filter(fecha, generador_funciones)
    id_funciones = [funcion.id for funcion in funciones_dentro_fecha]
    # print(id_funciones)
    reservas_dentro_fecha = filter(lambda reserva: reserva.id_funcion in id_funciones,
                                   generador_reservas)
    id_personas_dentro_fecha = {reserva.id_persona for reserva in reservas_dentro_fecha}

    return filter(lambda persona: persona.id not in id_personas_dentro_fecha, generador_personas)
