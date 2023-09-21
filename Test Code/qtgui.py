def dijkstra(N, INI, FIN, PRECIOS):
    # Inicializar las distancias y la lista de visitados
    distancias = [float('inf')] * N
    distancias[INI] = 0
    visitados = [False] * N
    
    # Cola de prioridad para seleccionar el siguiente nodo a visitar
    cola = [(0, INI)]  # (distancia, nodo)
    
    # Lista para guardar la ruta más corta
    ruta = [-1] * N
    
    while cola:
        # Obtener el nodo con la distancia más corta
        cola.sort()
        d, actual = cola.pop(0)
        
        # Si ya hemos visitado este nodo, pasamos al siguiente
        if visitados[actual]:
            continue
        
        # Marcar el nodo como visitado
        visitados[actual] = True
        
        # Actualizar las distancias y la ruta para cada vecino
        for vecino, peso in enumerate(PRECIOS[actual]):
            if peso == -1:
                continue  # No hay ruta desde este nodo al vecino
            distancia_nueva = distancias[actual] + peso
            if distancia_nueva < distancias[vecino]:
                distancias[vecino] = distancia_nueva
                ruta[vecino] = actual
                cola.append((distancia_nueva, vecino))
    
    # Reconstruir la ruta más corta
    ruta_corta = [FIN]
    actual = FIN
    while actual != INI:
        actual = ruta[actual]
        ruta_corta.append(actual)
    ruta_corta.reverse()
    
    # Retornar el precio de la ruta más corta y la ruta misma
    return [distancias[FIN], ruta_corta]

