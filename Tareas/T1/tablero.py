import copy
from pieza_explosiva import PiezaExplosiva
from imprimir_tablero import imprimir_tablero


class Tablero:
    def __init__(self, tablero: list) -> None:
        # filas         #columnas
        self.dimensiones = [len(tablero), len(tablero[0])]
        self.tablero = tablero

    @property
    def desglose(self) -> list:
        lista_desglose = [0, 0, 0]  # [XN, PP, --]
        for y in range(len(self.tablero)):
            # [["V2", "PP", "--", ...], ["H1", "--", "--", ...], ...]
            for x in range(len(self.tablero[y])):
                # ["V2", "PP", "--", ...]
                if self.tablero[y][x] == "PP":
                    lista_desglose[1] += 1
                elif self.tablero[y][x] == "--":
                    lista_desglose[2] += 1
                else:
                    lista_desglose[0] += 1
        return lista_desglose

    @property
    def peones_invalidos(self) -> int:
        p_inv = 0
        rango_y = range(len(self.tablero))
        rango_x = range(len(self.tablero[0]))
        for y in rango_y:
            for x in rango_x:
                n = 0
                if self.tablero[y][x] == "PP":
                    if (y + 1) in rango_y and self.tablero[y + 1][x] == "PP":
                        n += 1
                    if (y - 1) in rango_y and self.tablero[y - 1][x] == "PP":
                        n += 1
                    if (x + 1) in rango_x and self.tablero[y][x + 1] == "PP":
                        n += 1
                    if (x - 1) in rango_x and self.tablero[y][x - 1] == "PP":
                        n += 1
                    if n > 1:
                        p_inv += 1
        return p_inv

    @property
    def piezas_explosivas_invalidas(self) -> int:
        exp_inv = 0
        tab_sin_peones = copy.deepcopy(self.tablero)
        for y in range(len(tab_sin_peones)):
            for x in range(len(tab_sin_peones[y])):
                pieza = tab_sin_peones[y][x]
                if pieza == "PP":
                    tab_sin_peones[y][x] = "--"
        instancia_sin_peones = Tablero(tab_sin_peones)
        for y in range(len(tab_sin_peones)):
            for x in range(len(tab_sin_peones[y])):
                pieza = tab_sin_peones[y][x]
                if pieza != "PP" and pieza != "--":
                    if int(instancia_sin_peones.celdas_afectadas(y, x)) < \
                            int(pieza[1:]):
                        exp_inv += 1
        return exp_inv

    @property
    def tablero_transformado(self) -> list:
        t_transformado = self.tablero.copy()
        for y in range(len(t_transformado)):
            for x in range(len(t_transformado[y])):
                if t_transformado[y][x] != "PP" and \
                        t_transformado[y][x] != "--":
                    alcance = int(t_transformado[y][x][1:])
                    tipo = t_transformado[y][x][0]
                    posicion = [y, x]
                    t_transformado[y][x] = PiezaExplosiva(alcance,
                                                          tipo, posicion)
        return t_transformado

    def celdas_afectadas(self, fila: int, columna: int) -> int:
        rango_y = range(len(self.tablero))
        rango_x = range(len(self.tablero[0]))
        if self.tablero[fila][columna] != "PP" and \
                self.tablero[fila][columna] != "--":
            tipo = self.tablero[fila][columna][0]
            afectadas = 1
            if tipo in ["V", "R"]:
                peon_arriba = False
                peon_abajo = False
                for salto in range(1, len(self.tablero)):
                    fila_evaluada_arriba = fila - salto
                    fila_evaluada_abajo = fila + salto
                    if (fila_evaluada_arriba in rango_y
                            and self.tablero[fila_evaluada_arriba][columna]
                            == "PP"):
                        peon_arriba = True
                    if (fila_evaluada_abajo in rango_y and
                            self.tablero[fila_evaluada_abajo][columna]
                            == "PP"):
                        peon_abajo = True
                    if fila_evaluada_arriba in rango_y and not peon_arriba:
                        afectadas += 1
                    if fila_evaluada_abajo in rango_y and not peon_abajo:
                        afectadas += 1
            if tipo in ["H", "R"]:
                peon_izquierda = False
                peon_derecha = False
                for i in range(1, len(self.tablero[fila])):
                    col_ev_izq = columna - i
                    col_ev_der = columna + i
                    if col_ev_izq in rango_x and \
                            self.tablero[fila][col_ev_izq] == "PP":
                        peon_izquierda = True
                    if col_ev_der in rango_x and \
                            self.tablero[fila][col_ev_der] == "PP":
                        peon_derecha = True
                    if col_ev_izq in rango_x and not peon_izquierda:
                        afectadas += 1
                    if col_ev_der in rango_x and not peon_derecha:
                        afectadas += 1
            if tipo == "R":
                rango = 0
                if len(self.tablero[fila]) <= len(self.tablero):
                    rango = len(self.tablero)
                else:
                    rango = len(self.tablero[fila])
                peon_d1 = False
                peon_d2 = False
                peon_d3 = False
                peon_d4 = False
                for i in range(1, rango):
                    diag_1 = [fila - i, columna + i]
                    diag_2 = [fila + i, columna + i]
                    diag_3 = [fila + i, columna - i]
                    diag_4 = [fila - i, columna - i]
                    if (diag_1[0] in rango_y and diag_1[1] in rango_x and
                            self.tablero[diag_1[0]][diag_1[1]] == "PP"):
                        peon_d1 = True
                    if (diag_2[0] in rango_y and diag_2[1] in rango_x and
                            self.tablero[diag_2[0]][diag_2[1]] == "PP"):
                        peon_d2 = True
                    if (diag_3[0] in rango_y and diag_3[1] in rango_x and
                            self.tablero[diag_3[0]][diag_3[1]] == "PP"):
                        peon_d3 = True
                    if (diag_4[0] in rango_y and diag_4[1] in rango_x and
                            self.tablero[diag_4[0]][diag_4[1]] == "PP"):
                        peon_d4 = True
                    if diag_1[0] in rango_y and diag_1[1] in rango_x \
                            and not peon_d1:
                        afectadas += 1
                    if diag_2[0] in rango_y and diag_2[1] in rango_x \
                            and not peon_d2:
                        afectadas += 1
                    if diag_3[0] in rango_y and diag_3[1] in rango_x \
                            and not peon_d3:
                        afectadas += 1
                    if diag_4[0] in rango_y and diag_4[1] in rango_x \
                            and not peon_d4:
                        afectadas += 1
            return afectadas
        else:
            return -1

    def limpiar(self) -> int:
        for y in range(len(self.tablero)):
            for x in range(len(self.tablero[y])):
                if self.tablero[y][x] == "PP":
                    self.tablero[y][x] = "--"

    def reemplazar(self, nombre_nuevo_tablero: str) -> bool:
        try:
            archivo = open("tableros.txt", "r")
            lista_tableros = archivo.readlines()
            archivo.close()
            for i in range(len(lista_tableros)):
                i_tablero = lista_tableros[i].strip()
                i_tablero = i_tablero.split(",")
                nombre = i_tablero[0]
                if nombre_nuevo_tablero == nombre:
                    n_filas = int(i_tablero[1])
                    n_columnas = int(i_tablero[2])
                    indice = 3
                    nuevo_tablero = []
                    for y in range(n_filas):
                        fila = []
                        for x in range(n_columnas):
                            fila.append(i_tablero[indice])
                            indice += 1
                        nuevo_tablero.append(fila)
                    self.tablero.clear()
                    self.tablero.extend(nuevo_tablero)
                    self.dimensiones = [n_filas, n_columnas]
                    return True
            return False
        except FileNotFoundError:
            return False

    def solucionar(self) -> list:
        def solucionar_recursivo(tablero_actual, tableros_probados):
            instancia_actual = Tablero(tablero_actual)
            lista_cel_vacia = instancia_actual.lista_cel_vacias
            lista_p_exp = instancia_actual.lista_p_exp
            p_exp_inv = instancia_actual.p_exp_inv_con_PP
            peones_inv = instancia_actual.peones_invalidos
            solucionado = (peones_inv == 0) and (p_exp_inv == 0)
            if solucionado:
                return tablero_actual
            elif instancia_actual.piezas_explosivas_invalidas > 0 or \
                    instancia_actual.peones_invalidos > 0:
                return []
            for cel_vacia in lista_cel_vacia:
                tablero_temp = copy.deepcopy(tablero_actual)
                tablero_temp[cel_vacia[0]][cel_vacia[1]] = "PP"
                tablero_temp_str = self.tablero_a_texto(tablero_temp)
                if tablero_temp_str not in tableros_probados:
                    tableros_probados.add(tablero_temp_str)
                    instancia_temp = Tablero(tablero_temp)
                    pp_inv_temp = instancia_temp.peones_invalidos
                    validez = True
                    aporta = False
                    for p_exp in lista_p_exp:
                        celdas_afectadas = instancia_actual.celdas_afectadas(
                            p_exp[0], p_exp[1])
                        celdas_afectadas_esperadas = \
                            int(tablero_actual[p_exp[0]][p_exp[1]][1:])
                        delta = celdas_afectadas - celdas_afectadas_esperadas
                        celdas_afectadas_temp = \
                            instancia_temp.celdas_afectadas(p_exp[0], p_exp[1])
                        delta_temp = celdas_afectadas_temp - \
                            celdas_afectadas_esperadas
                        if (celdas_afectadas_temp < celdas_afectadas_esperadas
                                or pp_inv_temp != 0):
                            validez = False
                            break
                        elif 0 <= delta_temp < delta:
                            aporta = True
                    if validez and aporta:
                        avance = solucionar_recursivo(tablero_temp,
                                                      tableros_probados)
                        if avance != []:
                            return avance
            return []
        return solucionar_recursivo(self.tablero, set())

    @property
    def p_exp_inv_con_PP(self) -> int:
        tablero = self.tablero
        lista_p_exp = []
        for y in range(len(tablero)):
            for x in range(len(tablero[y])):
                if tablero[y][x] != "--" and tablero[y][x] != "PP":
                    lista_p_exp.append([y, x])
        p_exp_inv = 0
        for p_exp in lista_p_exp:
            if (int(self.celdas_afectadas(p_exp[0], p_exp[1])) !=
                    int(tablero[p_exp[0]][p_exp[1]][1:])):
                p_exp_inv += 1
        return p_exp_inv

    @property
    def lista_p_exp(self) -> list:
        lista_p_exp = []
        for y in range(len(self.tablero)):
            for x in range(len(self.tablero[y])):
                if self.tablero[y][x] != "--" and self.tablero[y][x] != "PP":
                    lista_p_exp.append([y, x])
        return lista_p_exp

    @property
    def lista_cel_vacias(self) -> list:
        lista_cel_vacia = []
        for y in range(len(self.tablero)):
            for x in range(len(self.tablero[y])):
                if self.tablero[y][x] == "--":
                    lista_cel_vacia.append([y, x])
        return lista_cel_vacia

    def tablero_a_texto(self, tablero):
        tablero_str = ""
        for fila in tablero:
            for indice in range(len(fila)):
                casilla = fila[indice]
                if casilla == "PP":
                    tablero_str += "P"
                else:
                    tablero_str += "X"
        return tablero_str
