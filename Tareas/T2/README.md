# Tarea 2: DCConejoChico


## Consideraciones generales :octocat:

La tarea cumple con todo lo solicitado en el enunciado y en la distribución de puntaje.
- Tanto el archivo main.py del cliente como el archivo main.py del servidor reciben como argumento de línea de comandos el número de puerto para efectuar la conexión por networking.
- La interfaz gráfica se muestra correctamente, estando pensada para ejecutarse en un computador con una resolución mayor a 1280x720. Además, el juego no espera que se intente cambiar su tamaño o maximizar.


### Cosas implementadas y no implementadas :white_check_mark: :x:

* Entrega Intermedia: ✅
* Entrega Final: ✅
    * Ventana Inicio: Hecha completa
    * Ventana Juego: Hecha completa
    * ConejoChico: Hecha completa
    * Lobos: Hecha completa
    * Cañón de Zanahorias: Hecha completa
    * Bomba Manzana: Hecha completa
    * Bomba Congeladora: Hecha completa
    * Fin del nivel: Hecha completa
    * Fin del Juego: Hecha completa
    * Recoger (G): Hecha completa
    * Pausa: Hecha completa
    * K+I+L: Hecha completa
    * I+N+F: Hecha completa
    * Networking: Hecha completa
    * Decodificación: Hecha completa
    * Desencriptación: Hecha completa
    * Archivos: Hecha completa
    * Funciones:  Hecha completa [Solo se reutilizaron las necesarias]

## Ejecución :computer:
Los módulos principales de la tarea a ejecutar son: ```main.py``` para el cliente, que está dentro de su respectiva carpeta y ```main.py``` para el servidor, que también está dentro de su carpeta respectiva. Además el programa espera que existan los siguientes archivos:
1. Dentro del servidor:
    - ```puntajes.txt``` en ```/servidor```
    - ```usuarios_bloqueados.txt``` en ```/servidor```
    - ```parametros_servidor.JSON``` en ```/servidor```
2. Dentro del cliente:
    - [```parametros_cliente.JSON```] en ```/cliente```
    - [```tablero_1.txt```, ```tablero_2.txt```, ```tablero_3.txt```] en ```/cliente/assets/laberintos```
    - [```derrota.mp3```, ```victoria.mp3```] en ```/cliente/assets/sonidos```
    - [```bloque_fondo.jpeg```, ```bloque_pared.jpeg```, ```canon_abajo.png```, ```canon_arriba.png```, ```canon_derecha.png```, ```canon_izquierda.png```, ```conejo.png```, ```conejo_abajo_1.png```, ```conejo_abajo_2.png```, ```conejo_abajo_3.png```, ```conejo_arriba_1.png```, ```conejo_arriba_2.png```, ```conejo_arriba_3.png```, ```conejo_derecha_1.png```, ```conejo_derecha_2.png```, ```conejo_derecha_3.png```, ```conejo_izquierda_1.png```, ```conejo_izquierda_2.png```, ```conejo_izquierda_3.png```, ```congelacion.png```, ```congelacion_burbuja.png```, ```explosion.png```, ```lobo_horizontal_derecha_1.png```, ```lobo_horizontal_derecha_2.png```, ```lobo_horizontal_derecha_3.png```, ```lobo_horizontal_izquierda_1.png```, ```lobo_horizontal_izquierda_2.png```, ```lobo_horizontal_izquierda_3.png```, ```lobo_vertical_abajo_1.png```, ```lobo_vertical_abajo_2.png```, ```lobo_vertical_abajo_3.png```, ```lobo_vertical_arriba_1.png```, ```lobo_vertical_arriba_2.png```, ```lobo_vertical_arriba_3.png```, ```logo.png```, ```manzana.png```, ```manzana_burbuja.png```, ```zanahoria_abajo.png```, ```zanahoria_arriba.png```, ```zanahoria_derecha.png```, ```zanahoria_izquierda.png```] en ```/cliente/assets/sprites```.



3. Dentro de ambos:
    - ```parametros.py```: contiene los parametros modificables del programa.

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```abc```: ```abstractmethod```
2. ```PyQt6```: ```QtCore```, ```QtWidgets```, ```QtGui```, ```QtMultimedia```  (debe instalarse)
3. ```os```
4. ```socket```
5. ```json```
6. ```pickle```
7. ```sys```
8. ```random```: ```randint()```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:
- ```\cliente```:
    1. ```casillas```: Contiene a ```Casilla```, ```Casilla_vacia```, ```Entrada```, ```Salida```, ```Bomba```, ```Bomba_explosion```, ```Pared```, ```Canon```, ```Entidad```, ```Enemigo```, ```Zanahoria```, ```Lobo```, ```Conejochico```, ```Timer_tiempo```. Estas clases son utilizadas por ```Tablero```, corresponden a las instancias de las casillas del juego.
    2. ```cliente```: Contiene a ```Cliente```, ```Listen_server_thread```. Encargado de comunicar al cliente (jugador) con el servidor, y procesar los mensajes entre la logica del juego y la interfaz grafica.
    3. ```logica```: Contiene a ```verificar_nombre()```, ```serializar_mensaje()```, ```separar_mensaje()```, ```encriptar_mensaje()```, ```codificar_mensaje()```. Encargado de manejar la funcion para validar localmente el nombre de usuario introducido, junto con las funciones para codificar los mensajes a enviar al servidor.
    4. ```obtener_paths```: Contiene a ```obtener_paths_tableros()```, ```obtener_paths_sprites()```. Encargado de manejar la correcta obtencion de los paths del tablero y de los sprites.
    5. ```partida```: Contiene a ```Partida```. Se encarga de la logica de juego a nivel partida, instanciando nuevos tableros y comunicando al cliente el estado de la partida.
    6. ```tablero```: Contiene a ```Tablero```. Encargado de la logica del juego a nivel tablero, manejando las entidades y casillas correspondientes. Se desecha al morir o al pasar de nivel por ```Partida```, para luego instanciar otro ```Tablero``` si corresponde.
- ```\servidor```:
    1. ```servidor```: Contiene a ```Servidor```, ```Listen_client_thread```. Se encarga de manejar, validar y responder las solicitudes de los clientes, ademas de guardar los puntajes y enviar el "salon de la fama".
    
## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. La carpeta assets sera añadida dentro de la carpeta del cliente (```/cliente/assets```) con todos los archivos necesarios, como los tableros, sprites y audios.
2. El usuario no intentara cambiar el tamaño de la ventana.
3. Los parametros modificables tendran valores razonables (la velocidad no será negativa o nula, etc.).

Recalco: ```no intentar cambiar el tamaño de la ventana```.
