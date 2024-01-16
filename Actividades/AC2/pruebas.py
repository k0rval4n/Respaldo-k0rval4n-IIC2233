from funciones import cargar_peliculas, cargar_generos, obtener_directores, obtener_str_titulos, filtrar_peliculas, \
    filtrar_peliculas_por_genero, DCCMax


#print(obtener_directores(cargar_peliculas("archivos/peliculas.csv")))
iterable = filtrar_peliculas(cargar_peliculas("archivos/peliculas.csv"), rating_max=9)
#iterable = DCCMax(list(cargar_peliculas("archivos/peliculas.csv")))
for i in iterable:
    print(i)