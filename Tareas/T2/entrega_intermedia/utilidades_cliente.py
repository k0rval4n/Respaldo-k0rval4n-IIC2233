def riesgo_derecha(coords: tuple, tablero: list):
    fil_i = coords[0]
    col_i = coords[1]
    choco = False
    for col in range(col_i + 1, len(tablero[fil_i])):
        if tablero[fil_i][col] == "P":
            choco = True
        if not choco and tablero[fil_i][col] == "C":
            return True
    return False


def riesgo_izquierda(coords: tuple, tablero: list):
    fil_i = coords[0]
    col_i = coords[1]
    choco = False
    for resta in range(1, col_i + 1):
        col = col_i - resta
        if tablero[fil_i][col] == "P":
            choco = True
        if not choco and tablero[fil_i][col] == "C":
            return True
    return False


def riesgo_abajo(coords: tuple, tablero: list):
    fil_i = coords[0]
    col_i = coords[1]
    choco = False
    for fil in range(fil_i + 1, len(tablero)):
        if tablero[fil][col_i] == "P":
            choco = True
        if not choco and tablero[fil][col_i] == "C":
            return True
    return False


def riesgo_arriba(coords: tuple, tablero: list):
    fil_i = coords[0]
    col_i = coords[1]
    choco = False
    for resta in range(1, fil_i + 1):
        fil = fil_i - resta
        if tablero[fil][col_i] == "P":
            choco = True
        if not choco and tablero[fil][col_i] == "C":
            return True
    return False
