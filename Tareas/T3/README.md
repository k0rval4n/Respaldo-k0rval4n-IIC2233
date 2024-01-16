# Tarea 3: DCCine 🎬🎥


## Consideraciones generales :octocat:

La tarea cumple con todo lo solicitado en el enunciado y en la distribución de puntaje.

### Cosas implementadas y no implementadas :white_check_mark: :x:


####  Programación funcional
##### ✅ Utiliza 1 generador
Se implementan todas las funciones solicitadas que reciben 1 generador.
##### ✅ Utiliza 2 generadores
Se implementan todas las funciones solicitadas que reciben 2 generadores.
##### ✅ Utiliza 3 o más generadores
Se implementan todas las funciones solicitadas que reciben 3 o más generadores.
####  API
##### ✅ Obtener información
Se implementan todos los métodos solicitados de la clase ```Pelicula``` que se encargan de obtener informacion.
##### ✅ Modificar información
Se implementan todos los métodos solicitados de la clase ```Pelicula``` que se encargan de modificar información, ya sea para crear, añadir o eliminar.

## Ejecución :computer:
Los módulos principales de la tarea a ejecutar son  ```consultas.py``` para el apartado de Programación Funcional y ```peli.py``` para el apartado de Web Services.


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

-> consultas y peli:
1. ```functools```: ```reduce()```
2. ```math```
3. ```typing```: ```Generator```
4. ```requests``` (debe instalarse)

-> utilidades:
1. ```collections```: ```namedtuple```

-> api:
1. ```wsgiref.simple_server```: ```make_server```, ```WSGIRequestHandler```
2. ```threading```
3. ```json```
4. ```urllib.parse```: ```parse_qs```
5. ```datetime```: ```date```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```consultas```: Contiene las funciones solicitadas en el apartado de Programación Funcional.
2. ```peli```: Contiene la clase ```Peliculas```, la cual tiene los métodos solicitados en el apartado de Web Services.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Los archivos ```api.py``` y ```utilidades.py``` estarán presentes al momento de ejecutar el programa.


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. [https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary](https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary): el código no esta explicito, pero se utilizo en el archivo [```consultas.py```](/consultas.py) para la función [```genero_comun()```](/consultas.py#L204) para que la función [```max()```](/consultas.py#L220) efectivamente obtenga el máximo.

## Descuentos
La guía de descuentos se encuentra aquí: [link](https://github.com/IIC2233/Syllabus/blob/main/Tareas/Bases%20Generales%20de%20Tareas%20-%20IIC2233.pdf).