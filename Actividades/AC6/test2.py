from collections import defaultdict
from functools import wraps
from io import StringIO
import signal
import unittest
from unittest.mock import patch

from equipo import Jugador, Equipo


# Clase que ejecuta los tests
class VerificarEquipo(unittest.TestCase):
    """
    Clase para ejecutar el conjunto de tests de la actividad.
    """

    def __init__(self) -> None:
        """
        Prepara un grafo de equipo para cada test,
        agregándole jugadores y relaciones.
        """
        self.equipo = Equipo()
        self.equipo.jugadores = {
            0: Jugador('Alan', 2),
            1: Jugador('Alberto', 3),
            2: Jugador('Alejandra', 5),
            3: Jugador('Alex', 8),
            4: Jugador('Alonso', 13),
            5: Jugador('Alba', 21),
            6: Jugador('Alicia', 34),
            7: Jugador('Alfredo', 55),
            8: Jugador('Alma', 16),
            9: Jugador('Aldo', 89)
        }
        adyacencia = {
            0: [1],
            1: [0, 2, 3],
            2: [1, 3],
            3: [1],
            4: [5],
            5: [4, 6],
            6: [4, 5],
            7: [8],
            8: [9],
            9: list()
        }
        self.equipo.dict_adyacencia = defaultdict(list)
        for key, value in adyacencia.items():
            self.equipo.dict_adyacencia[key] = value


    def test_agregar_jugador_correcto(self):
        """
        Prueba que un jugador pueda agregarse correctamente al equipo
        """
        new = Jugador('Alejo', 10)
        ret = self.equipo.agregar_jugador(10, new)
        print(len(self.equipo.jugadores) == 11)
        self.assertFalse(ret)

    
    def test_agregar_jugador_fallido(self):
        """
        Prueba el caso donde se trata de agregar un jugador con un id
        que ya existe en el equipo
        """
        new = Jugador('Alejo', 10)
        ret = self.equipo.agregar_jugador(9, new)
        print(len(self.equipo.jugadores) == 10)
        self.assertTrue(ret)

    
    def test_agregar_vecinos_correcto(self):
        """
        Prueba el caso donde se agregan correctamente
        vecinos nuevos a un jugador y la funcion retorna el valor correcto.
        Comprueba que el agregar vecinos no sea mutuo.
        """
        ret = self.equipo.agregar_vecinos(8, [7, 9])
        self.assertSetEqual(set(self.equipo.dict_adyacencia[8]), {7, 9})
        print(len(self.equipo.dict_adyacencia[9]) == 0)
        print(ret == 1)

    
    def test_agregar_vecinos_fallido(self):
        """
        Prueba el caso donde se tratan de agregar vecinos a un id de jugador
        que no existe.
        """
        ret = self.equipo.agregar_vecinos(10, [])
        print(ret == -1)

    
    def test_peor_amigo_correcto(self):
        """
        Prueba que peor_amigo esté encontrando al jugador correcto.
        """
        ret = self.equipo.peor_amigo(5)
        print(ret == self.equipo.jugadores[6])

    
    def test_peor_amigo_fallido(self):
        """
        Prueba que peor_amigo entregue None cuando el jugador no tiene vecinos.
        """
        ret = self.equipo.peor_amigo(9)
        self.assertIsNone(ret)

    
    def test_mejor_companero_correcto(self):
        """
        Prueba que mejor_compañero este encontrando al jugador correcto.
        """
        ret = self.equipo.mejor_compañero(0)
        print(ret == self.equipo.jugadores[1])

    
    def test_mejor_companero_fallido(self):
        """
        Prueba que mejor_compañero entregue None
        cuando el jugador es el unico miembro del equipo.
        """
        self.equipo.jugadores = {9: Jugador('Aldo', 89)}
        self.equipo.dict_adyacencia = {9: {}}
        ret = self.equipo.mejor_compañero(9)
        self.assertIsNone(ret)

    
    def test_mejor_conocido_unico(self):
        """
        Prueba que mejor_conocido funcione con un camino de largo 2
        """
        ret = self.equipo.mejor_conocido(7)
        print(ret == self.equipo.jugadores[9])

    
    def test_mejor_conocido_simple(self):
        """
        Prueba que mejor_conocido funcione con caminos de complejidad simple.
        """
        ret = self.equipo.mejor_conocido(4)
        print(ret == self.equipo.jugadores[5])

    
    def test_mejor_conocido_complejo(self):
        """
        Prueba que mejor_conocido funcione con caminos de mayor complejidad.
        """
        ret = self.equipo.mejor_conocido(0)
        print(ret == self.equipo.jugadores[1])

    
    def test_mejor_conocido_none(self):
        """
        Prueba que mejor_conocido retorne None cuando el jugador no
        tiene vecinos.
        """
        ret = self.equipo.mejor_conocido(9)
        self.assertIsNone(ret)

    
    def test_distancia_self(self):
        """
        Prueba que distancia de un jugador a si mismo sea 0.
        """
        ret = self.equipo.distancia(7, 7)
        print(ret == 0)

    
    def test_distancia_simple(self):
        """
        Prueba que la distancia entre vecinos directos sea 1.
        """
        ret = self.equipo.distancia(7, 8)
        print(ret == 1)

    
    def test_distancia_complejo(self):
        """
        Prueba que la distancia entre vecinos no directos esté
        bien calculada.
        """
        ret = self.equipo.distancia(0, 3)
        print(ret == 2)
        ret = self.equipo.distancia(0, 2)
        print(ret == 2)

    
    def test_distancia_none(self):
        """
        Prueba que la distancia entre nodos que no tengan
        un camino sea -1
        """
        ret = self.equipo.distancia(0, 9)
        print(ret == -1)

    
    def test_distancia_jugador_invalido(self):
        """
        Prueba que la distancia para algún jugador que no
        exista y otro sea -1
        """
        ret = self.equipo.distancia(0, 10)
        print(ret == -1)


if __name__ == '__main__':
    verificar_equipo = VerificarEquipo()
    verificar_equipo.test_distancia_self()
    verificar_equipo.test_distancia_simple()
    verificar_equipo.test_distancia_none()
    verificar_equipo.test_distancia_complejo()
    verificar_equipo.test_distancia_jugador_invalido()