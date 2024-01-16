# PARAMETROS VENTANA
ANCHO_LABERINTO = 16
LARGO_LABERINTO = 16
ANCHO_VENTANA = 1280
LARGO_VENTANA = 720
# PATHS
DICCIONARIO_PATHS_SPRITES = {
    "LL": ["lobo_horizontal_izquierda_1.png", "lobo_horizontal_izquierda_2.png",
           "lobo_horizontal_izquierda_3.png"],
    "LR": ["lobo_horizontal_derecha_1.png", "lobo_horizontal_derecha_2.png",
           "lobo_horizontal_derecha_3.png"],
    "LU": ["lobo_vertical_arriba_1.png", "lobo_vertical_arriba_2.png",
           "lobo_vertical_arriba_3.png"],
    "LD": ["lobo_vertical_abajo_1.png", "lobo_vertical_abajo_2.png", "lobo_vertical_abajo_3.png"],
    "ZL": ["zanahoria_izquierda.png"],
    "ZR": ["zanahoria_derecha.png"],
    "ZU": ["zanahoria_arriba.png"],
    "ZD": ["zanahoria_abajo.png"],
    "BM": ["manzana.png", "manzana_burbuja.png"],
    "BC": ["congelacion.png", "congelacion_burbuja.png"],
    "CU": ["canon_arriba.png"],
    "CD": ["canon_abajo.png"],
    "CL": ["canon_izquierda.png"],
    "CR": ["canon_derecha.png"],
    "P": ["bloque_pared.jpeg"],
    "-": ["bloque_fondo.jpeg"],
    "JR": ["conejo_derecha_1.png", "conejo_derecha_2.png",
           "conejo_derecha_3.png"],
    "JL": ["conejo_izquierda_1.png", "conejo_izquierda_2.png",
           "conejo_izquierda_3.png"],
    "JU": ["conejo_arriba_1.png", "conejo_arriba_2.png",
           "conejo_arriba_3.png"],
    "JD": ["conejo_abajo_1.png", "conejo_abajo_2.png",
           "conejo_abajo_3.png"],
    "XM": ["explosion.png"],
    "XC": ["congelacion.png"]
    }
PATH_TABLERO_1 = "tablero_1.txt"
PATH_TABLERO_2 = "tablero_2.txt"
PATH_TABLERO_3 = "tablero_3.txt"
# PARAMETROS JUEGO
DURACION_NIVEL_INICIAL = 60
VELOCIDAD_LOBO_INICIAL = 1
PONDERADOR_LABERINTO = 1
PUNTAJE_LOBO = 1
CANTIDAD_VIDAS = 3
VELOCIDAD_CONEJO = 10
VELOCIDAD_ZANAHORIA = 1
TIEMPO_BOMBA = 1
PUNTAJE_INF = 1
BOMBAS_M = 0
BOMBAS_C = 0
DICT_PARAMETROS_INICIALES = {
    "ANCHO_LABERINTO": ANCHO_LABERINTO,
    "LARGO_LABERINTO": LARGO_LABERINTO,
    "DURACION_NIVEL_INICIAL": DURACION_NIVEL_INICIAL,
    "VELOCIDAD_LOBO_INICIAL": VELOCIDAD_LOBO_INICIAL,
    "PONDERADOR_LABERINTO": PONDERADOR_LABERINTO,
    "PUNTAJE_LOBO": PUNTAJE_LOBO,
    "CANTIDAD_VIDAS": CANTIDAD_VIDAS,
    "VELOCIDAD_CONEJO": VELOCIDAD_CONEJO,
    "VELOCIDAD_ZANAHORIA": VELOCIDAD_ZANAHORIA,
    "TIEMPO_BOMBA": TIEMPO_BOMBA,
    "PUNTAJE_INF": PUNTAJE_INF,
    "BOMBAS_M": BOMBAS_M,
    "BOMBAS_C": BOMBAS_C
    }
