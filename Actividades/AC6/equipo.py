from collections import defaultdict, deque


class Jugador:
    def __init__(self, nombre: str, velocidad: int) -> None:
        self.nombre = nombre
        self.velocidad = velocidad

    def __repr__(self) -> None:
        return f'Jugador: {self.nombre}, Velocidad: {self.velocidad}'


class Equipo:
    def __init__(self) -> None:
        self.jugadores = dict()
        self.dict_adyacencia = defaultdict(list)

    def agregar_jugador(self, id_jugador: int, jugador: Jugador) -> bool:
        '''Agrega un nuevo jugador al equipo.'''
        if id_jugador not in self.jugadores.keys():
            self.jugadores[id_jugador] = jugador
            return False
        else:
            return True

    def agregar_vecinos(self, id_jugador: int, vecinos: list[int]) -> int:
        '''Agrega una lista de vecinos a un jugador.'''
        if id_jugador not in self.dict_adyacencia.keys():
            self.dict_adyacencia[id_jugador] = list()
            return -1
        else:
            n_antiguo = len(self.dict_adyacencia[id_jugador])
            lista_intermedia = list(set(self.dict_adyacencia[id_jugador] + vecinos))
            n_nuevo = len(lista_intermedia)
            self.dict_adyacencia[id_jugador] = lista_intermedia
            return n_nuevo - n_antiguo

    def peor_amigo(self, id_jugador: int) -> Jugador:
        '''Retorna al vecino con la velocidad menos similar.'''
        lista_id_vecinos = self.dict_adyacencia[id_jugador]
        lista_vecinos = []
        jugador = self.jugadores[id_jugador]
        for id in lista_id_vecinos:
            if id != id_jugador and id in self.jugadores.keys():
                lista_vecinos.append(self.jugadores[id])
        if len(lista_vecinos) > 0:
            return max(lista_vecinos, key=lambda vecino: abs(jugador.velocidad - vecino.velocidad))
        else:
            return None

    def mejor_compañero(self, id_jugador: int) -> Jugador:
        '''Retorna al compañero de equipo con la menor diferencia de velocidad.'''
        lista_id_vecinos = self.dict_adyacencia[id_jugador]
        lista_vecinos = []
        jugador = self.jugadores[id_jugador]
        for id in lista_id_vecinos:
            if id != id_jugador and id in self.jugadores.keys():
                lista_vecinos.append(self.jugadores[id])
        if len(lista_vecinos) > 0:
            return min(lista_vecinos, key=lambda vecino: abs(jugador.velocidad - vecino.velocidad))
        else:
            return None

    def mejor_conocido(self, id_jugador: int) -> Jugador:
        '''Retorna al conocido con la menor diferencia de velocidad.'''
        jugador = self.jugadores[id_jugador]
        id_visitados = []
        queue = deque([id_jugador])
        while len(queue) > 0:
            id = queue.popleft()
            if id in id_visitados:
                continue
            if id != id_jugador:
                id_visitados.append(id)
            for vecino in self.dict_adyacencia[id]:
                if vecino not in id_visitados:
                    queue.append(vecino)
        lista_vecinos = []
        for id in id_visitados:
            if id != id_jugador and id in self.jugadores.keys():
                lista_vecinos.append(self.jugadores[id])
        if len(lista_vecinos) > 0:
            return min(lista_vecinos, key=lambda vecino: abs(jugador.velocidad - vecino.velocidad))
        else:
            return None

    def distancia(self, id_jugador_1: int, id_jugador_2: int) -> int:
        '''Retorna el tamaño del camino más corto entre los jugadores.'''
        por_visitar = set()
        lista_caminos_recorridos = set()
        queue = deque([(id_jugador_1, tuple())])

        while len(queue) > 0:
            nodo, camino_recorrido = queue.popleft()
            if nodo == id_jugador_2:
                lista_caminos_recorridos.add(camino_recorrido)
            for vecino in self.dict_adyacencia[nodo]:
                if vecino not in por_visitar:
                    por_visitar.add(vecino)
                    queue.append((vecino, camino_recorrido + (vecino,)))
        if id_jugador_1 == id_jugador_2:
            return 0
        elif len(list(lista_caminos_recorridos)) > 0:
            return len(min(lista_caminos_recorridos, key=lambda lista: len(lista)))
        else:
            return -1


if __name__ == '__main__':
    equipo = Equipo()
    jugadores = {
        0: Jugador('Ana', 1),
        1: Jugador('Antonio', 3),
        2: Jugador('Alfredo', 6),
        3: Jugador('Ariel', 10)
    }
    adyacencia = {
        0: [1],
        1: [0, 2],
        2: [1],
    }
    for idj, jugador in jugadores.items():
        equipo.agregar_jugador(id_jugador=idj, jugador=jugador)
    for idj, vecinos in adyacencia.items():
        equipo.agregar_vecinos(id_jugador=idj, vecinos=vecinos)
    for idj, vecinos in adyacencia.items():
        equipo.agregar_vecinos(id_jugador=idj, vecinos=vecinos)
    print(equipo.jugadores)
    print(equipo.dict_adyacencia)
    print(f'El peor amigo de Antonio es {equipo.peor_amigo(1)}')
    print(f'El mejor compañero de Ana es {equipo.mejor_compañero(0)}')
    print(f'El mejor conocido de Alfredo es {equipo.mejor_conocido(2)}')
    print(f'La distancia entre Alfredo y Ana es {equipo.distancia(2, 0)}')
    print(f'La distancia entre Antonio y Ariel es {equipo.distancia(1, 3)}')
    print(f'La distancia entre Antonio y Amalia es {equipo.distancia(1, 5)}')
