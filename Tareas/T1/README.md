# Tarea 1: DCChexxploding 💥♟️

## Consideraciones generales :octocat:

La tarea cumple con todo lo solicitado en el enunciado y en la distribución de puntaje. Es decir:
- Los métodos de las clases entregadas fueron creados y cumplen su función.
- El archivo principal recibe como argumento de línea de comandos los argumentos solicitados. Además, se creó e implementó el menú de acciones, permitiendo al usuario interactuar con el programa y realizar lo solicitado.

### Cosas implementadas y no implementadas :white_check_mark: :x:


#### Menú: 18 pts (30%)
##### ✅ Consola: Se preparó el archivo [```main.py```](main.py) para ser ejecutado desde la línea de comandos. Se espera recibir dos argumentos en el siguiente orden: nombre_de_usuario, tablero_escogido. Sin embargo, se aborda el caso de borde en el que se entregue una cantidad distinta de argumentos. En este caso, se imprimirá un mensaje de error y el programa finalizará. Además, se verifica que el nombre de usuario y el tablero escogido cumplan solicitado: que el nombre tenga al menos 4 carácteres, todos del alfabeto. También se comprueba que el tablero escogido exista en la base de datos. Se imprime una alerta en cualquiera de los dos casos, de forma independiente, y el programa finalizará.

##### ✅ Menú de Acciones: El menú saluda al usuario mencionando el nombre de usuario entregado. Además, incluye las opciones ```[1] mostrar tablero```, ```[2] limpiar tablero```, ```[3] solucionar el tablero``` y ```[4] salir del programa```. Las opciones se eligen mediante un input introducido por el usuario. El programa mostará una alerta en caso de introducir un input distinto a 1, 2, 3 o 4 y procederá a mostrar nuevamente el menú, solicitando introducir una opción válida.
- ```[1] mostrar tablero```: Se llama a la función [```imprimir_tablero()```](/README.md?plain=1#L53) para mostrar en pantalla el tablero actualmente cargado.
- ```[2] limpiar tablero```: Elimina solo los peones del tablero cargado actualmente. Luego, reemplaza el tablero anterior con el limpio, es decir, que las opciones siguientes utilizarán el tablero sin peones.
- ```[3] solucionar el tablero```: Busca una solución al tablero cargado actualmente añadiendo peones para cumplir con las tres reglas de ```DCChexxploding```. En caso de que no exista solución para el tablero, se imprimirá un mensaje anunciando este hecho.
- ```[4] salir del programa```: Se termina la ejecución del programa.

##### ✅ Modularización: Se importaron correctamente los módulos requeridos. No se requirió la creación de nuevos archivos para reducir la cantidad de líneas.

##### ✅ PEP8: Se respetó el límite de 400 líneas máximo por archivo y 100 carácteres máximos por archivo. Además, se siguió el estándar CamelCase para los nombres de las clases y snake_case para el caso de las variables, métodos y funciones.


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es [```main.py```](main.py). Además se debe crear los siguientes archivos y directorios adicionales:
1. ```tableros.txt``` en ```/```. Archivo de texto que contiene los tableros disponibles en el formato: nombre_tablero, filas, columnas, (filas*columnas) piezas separadas por comas.


## Librerías :books:
### Librerías externas utilizadas ✅
La lista de librerías externas que utilicé fue la siguiente:

1. ```copy```: ```deepcopy()```
2. ```string```: ```ascii_lowercase```
3. ```sys```: ```argv```
4. ```os```: ```name, system()```


### Librerías propias ✅
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. [```tablero```](tablero.py): Contiene a la clase ```Tablero```, la cual tiene los siguientes métodos/propertys:
    - @property desglose
    - @property peones_invalidos
    - @property piezas_explosivas_invalidas
    - @property tablero_transformado
    - celdas_afectadas(fila: int, columna: int)
    - limpiar()
    - reemplazar(nombre_nuevo_tablero: str)
    - solucionar()
    - @property p_exp_inv_con_PP
    - @property lista_p_exp
    - @property lista_cel_vacias

2. [```pieza_explosiva```](pieza_explosiva.py): Contiene a la clase ```PiezaExplosiva```, la cual tiene los siguientes métodos/propertys:
    - verificar_alcance(fila: int, columna: int)

## Supuestos y consideraciones adicionales :thinking: ✅
Los supuestos que realicé durante la tarea son los siguientes:

1. El programa será ejecutado en sistemas Windows, Mac o Linux. Esto según se indicó al inicio del curso. Si esto no se cumple, la función [```limpiar()```](/README.md?plain=1#L103) no se ejecutará correctamente.
2. Se crearon las siguientes propertys adicionales para la clase [```Tablero```](tablero.py?plain=1#L6):
    - [```p_exp_inv_con_PP()```](tablero.py?plain=1#L246): Esta indica la cantidad de piezas explosivas inválidas que posee el tablero de la instancia evaluada.
    - [```lista_p_exp```](tablero.py?plain=1#L261): Esta guarda en una lista las coordenadas de los peones del tablero de la instancia evaluada en el formato [coordenada_y, coordenada_x].
    - [```lista_cel_vacias```](tablero.py?plain=1#L270): Esta guarda en una lista las coordenadas de las celdas vacías del tablero de la instancia evaluada en el formato [coordenada_y, coordenada_x].
3. Pese a que no está incluido en el repositorio, se espera que el archivo ```imprimir_tablero.py``` esté presente y contenga la función ```imprimir_tablero()``` a la hora de ejecutar la tarea.


## Referencias de código externo :book: ✅

Para realizar mi tarea saqué código de:
1. (https://micro.recursospython.com/recursos/como-limpiar-la-consola.html): este corresponde a la función ```limpiar()``` que permite limpiar la consola y está implementado en el archivo [```main.py```](main.py?plain=1#L8) en las líneas 8 a 12.
2. (https://geekflare.com/es/check-if-file-folder-exists-in-python/): este corresponde a la excepción ```FileNotFoundError```, que permite abordar el caso en que el archivo ```tableros.txt``` no exista. Está implementado en el archivo [```main.py```](main.py?plain=1#L33) en las líneas 32 a 38 y en el archivo [```tablero.py```](tablero.py?plain=1#L172) en las lineas 172 a 197, método [```reemplazar()```](tablero.py?plain=1#L171).

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/Syllabus/blob/main/Tareas/Bases%20Generales%20de%20Tareas%20-%20IIC2233.pdf).