import sys
import string
import os
from imprimir_tablero import imprimir_tablero
from tablero import Tablero


def limpiar():
    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
        os.system("clear")


if __name__ == "__main__":
    # [nombre_archivo, arg1, arg2, ...]
    argumentos_por_consola = sys.argv
    dos_argumentos = len(argumentos_por_consola) == 3
    if dos_argumentos:
        nombre = argumentos_por_consola[1]
        nombre_tablero_elegido = argumentos_por_consola[2]
        alfabeto = string.ascii_lowercase[:14]+"ñ"+string.ascii_lowercase[14:]
        nombre_valido = True
        nombre_tablero_existe = True
        archivo_tableros_existe = True
        if len(nombre) < 4:
            nombre_valido = False
        for caracter in nombre:
            if caracter.lower() not in alfabeto:
                nombre_valido = False
        lista_lineas_archivo = []
        try:
            archivo = open("tableros.txt", "r")
            lista_lineas_archivo = archivo.readlines()
            archivo.close()
        except FileNotFoundError:
            archivo_tableros_existe = False
            print(f"-> ¡El archivo \"tableros.txt\" no existe!")
        lista_nombres_tableros = []
        for i in range(len(lista_lineas_archivo)):
            i_tablero = lista_lineas_archivo[i].strip()
            i_tablero = i_tablero.split(",")
            lista_nombres_tableros.append(i_tablero[0])
        if nombre_tablero_elegido not in lista_nombres_tableros:
            nombre_tablero_existe = False
        if not nombre_valido:
            print(f"-> ¡El nombre \"{nombre}\" no es valido!")
        if not nombre_tablero_existe:
            print(f"-> ¡El tablero de nombre \"{nombre_tablero_elegido}\" \
no existe en la base de datos!")
        if nombre_valido and nombre_tablero_existe and \
                archivo_tableros_existe:
            instancia_tablero = Tablero([[""]])
            instancia_tablero.reemplazar(nombre_tablero_elegido)
        ejecutar = nombre_valido and nombre_tablero_existe and dos_argumentos
        while ejecutar:
            opcion = input(f"""
Hola {nombre}!

*** Menú de Acciones ***

[1] Mostrar tablero
[2] Limpiar tablero
[3] Solucionar tablero
[4] Salir del programa
Indique su opción (1, 2, 3 o 4): """)
            limpiar()
            tablero_elegido = instancia_tablero.tablero
            if opcion not in ["1", "2", "3", "4"]:
                print("""-> ¡La opcion seleccionada no es valida!""")
            elif int(opcion) == 1:
                print("-> El tablero actual es:\n")
                imprimir_tablero(tablero_elegido)

            elif int(opcion) == 2:
                instancia_tablero.limpiar()
                print("-> ¡El tablero ha sido limpiado!")

            elif int(opcion) == 3:
                print("-> Buscando solucion...\n")
                sol = instancia_tablero.solucionar()
                if sol != []:
                    print("-> Una solucion al tablero entregado es:\n")
                    imprimir_tablero(sol)
                else:
                    print("-> ¡El tablero entregado no tiene \
solucion posible!")

            elif int(opcion) == 4:
                ejecutar = False
    else:
        print("""
-> ¡No introdujo solo dos argumentos
   por consola en el formato \"main.py
   nombre_usuario nombre_tablero\"!""")
