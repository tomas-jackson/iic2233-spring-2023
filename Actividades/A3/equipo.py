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
        self.dict_adyacencia = defaultdict(set)
    
    def agregar_jugador(self, id_jugador: int, jugador: Jugador) -> bool:
        '''Agrega un nuevo jugador al equipo.'''
        if id_jugador in self.jugadores:
            return False
        else:
            self.jugadores[id_jugador] = jugador
            self.dict_adyacencia[id_jugador] = set()
            return True

    def agregar_vecinos(self, id_jugador: int, vecinos: list[int]) -> int:
        '''Agrega una lista de vecinos a un jugador.'''
        if id_jugador not in self.dict_adyacencia:
            return -1
        else:
            q_added = len(vecinos)
            for player in vecinos:
                if player in self.dict_adyacencia[id_jugador]:
                    q_added -= 1
                self.dict_adyacencia[id_jugador].add(player)
            return q_added

    def mejor_amigo(self, id_jugador: int) -> Jugador:
        '''Retorna al vecino con la velocidad más similar.'''
        minimum = float('inf')
        actual = -1
        for vecinos_id in self.dict_adyacencia[id_jugador]:
            speed_diff = abs(self.jugadores[id_jugador].velocidad - self.jugadores[vecinos_id].velocidad)
            if speed_diff < minimum:
                minimum = speed_diff
                actual = vecinos_id
        if actual == -1:
            return None
        else:
            return self.jugadores[actual]

    def peor_compañero(self, id_jugador: int) -> Jugador:
        '''Retorna al compañero de equipo con la mayor diferencia de velocidad.'''
        maximum = 0
        actual = -1
        for vecino in self.jugadores.values():
            speed_diff = abs(self.jugadores[id_jugador].velocidad - vecino.velocidad)
            if speed_diff > maximum:
                maximum = speed_diff
                actual = vecino
        if actual == -1:
            return None
        else:
            return actual

    def peor_conocido(self, id_jugador: int) -> Jugador:
        '''Retorna al amigo con la mayor diferencia de velocidad.'''
        visitados = []
        cola = deque([id_jugador])
        while len(cola) > 0:
            vertice = cola.popleft()
            if vertice in visitados:
                continue
            visitados.append(vertice)

            for vecino in self.dict_adyacencia[vertice]:
                if vecino not in visitados:
                    cola.append(vecino)
        maximum = 0
        actual = -1
        for vecinos_id in visitados:
            speed_diff = abs(self.jugadores[id_jugador].velocidad - self.jugadores[vecinos_id].velocidad)
            if speed_diff > maximum:
                maximum = speed_diff
                actual = vecinos_id
        if actual == -1:
            return None
        else:
            return self.jugadores[actual]

    def distancia(self, id_jugador_1: int, id_jugador_2: int) -> int:
        '''Retorna el tamaño del camino más corto entre los jugadores.'''
        rutas = [[id_jugador_1]]
        ruta_index = 0
        visitados = set([id_jugador_1])

        if id_jugador_1 == id_jugador_2:
            mas_corta = 0
            return mas_corta

        while ruta_index < len(rutas):
            ruta_actual = rutas[ruta_index]
            ultimo_nodo = ruta_actual[-1]
            nodos_proximos = self.dict_adyacencia[ultimo_nodo]
            if id_jugador_2 in nodos_proximos:
                ruta_actual.append(id_jugador_2)
                mas_corta = len(ruta_actual) - 1
                return mas_corta
            for nodo_nuevo in nodos_proximos:
                if nodo_nuevo not in visitados:
                    nueva_ruta = ruta_actual[:]
                    nueva_ruta.append(nodo_nuevo)
                    rutas.append(nueva_ruta)
                    visitados.add(nodo_nuevo)
            ruta_index += 1
        return -1


if __name__ == '__main__':
    equipo = Equipo()
    jugadores = {
        0: Jugador('Alonso', 1),
        1: Jugador('Alba', 3),
        2: Jugador('Alicia', 6),
        3: Jugador('Alex', 10)
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
    
    print(f'El mejor amigo de Alba es {equipo.mejor_amigo(1)}') 
    print(f'El peor compañero de Alonso es {equipo.peor_compañero(0)}')
    print(f'El peor amigo de Alicia es {equipo.peor_compañero(2)}')
    print(f'La distancia entre Alicia y Alonso es {equipo.distancia(2, 0)}')
    print(f'La distancia entre Alba y Alex es {equipo.distancia(1, 3)}')
    