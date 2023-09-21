import os.path
from collections import deque


def formar_menu_acciones() -> str:
    """
    esta funcion retorna el menu de acciones para que pueda ser printeado
    """
    linea_1 = '[1] Mostrar tablero'
    linea_2 = '[2] Validar bombas y tortugas'
    linea_3 = '[3] Solucionar tablero'
    linea_4 = '[4] Validar solucion'
    linea_5 = '[0] Salir del DCCeldas'
    return f'\n**MENU DE ACCIONES**\n\n{linea_1}\n{linea_2}\n{linea_3}\n{linea_4}\n{linea_5}'


"""
las cuatro funciones siguientes son para checkear el valor arriba, abajo y a los lados
de una posicion especifica en una matriz, retorna True si son iguales a T, False en los otros casos
"""


def check_up(tablero, row, col):
    if row == 0:
        return False
    elif tablero[row - 1][col] == 'T':
        return True
    return False


def check_left(tablero, row, col):
    if col == 0:
        return False
    elif 'T' == tablero[row][col - 1]:
        return True
    return False


def check_right(tablero, row, col):
    if col == len(tablero) - 1:
        return False
    elif 'T' == tablero[row][col + 1]:
        return True
    return False


def check_down(tablero: list, row: int, col: int) -> bool:
    if row == len(tablero) - 1:
        return False
    elif tablero[row + 1][col] == 'T':
        return True
    return False


def contar_bloques(indice: int, fila: list) -> int:
    """
    esta funcion cuenta los espacios libres ('-') para cado lado de una posicion especifica en una
    fila retorna la cantidad de bloques vacios
    """
    left_check, right_check = True, True  # busca checkear para cada lado del indice
    counter, index_step_right, index_step_left = 0, 1, 1
    # counter cuenta las invalidas, index_step dice la distancia del indice que revisamos
    while left_check or right_check:
        if left_check is True:
            # si vamos a checkear fuera de la lista o si vamos a
            # checkear una tortuga, la revision de ese lado termina
            # en cualquier otro caso le sumamos uno al contador y uno a la distancia para checkear
            if indice - index_step_left < 0 or fila[indice - index_step_left] == 'T':
                left_check = False
            else:
                index_step_left, counter = index_step_left + 1, counter + 1
        if right_check is True:
            # misma logica que left check
            if indice + index_step_right > len(fila) - 1 or fila[indice + index_step_right] == 'T':
                right_check = False
            else:
                index_step_right, counter = 1 + index_step_right, 1 + counter
    return counter


def cargar_tablero(nombre_archivo: str) -> list:
    """
    esta funcion se usa para leer un archivo (el nombre que se entrega debe incluir extension) y
    retorna una lista de lista que representa al tablero
    """
    dir_archivo = os.path.join('Archivos', nombre_archivo)
    with open(dir_archivo, 'r') as info_archivo:
        info_tablero = deque(info_archivo.readline().split(','))
    square_size = int(info_tablero.popleft())
    tablero = [[] for i in range(square_size)]
    for row in tablero:
        for i in range(square_size):
            row.append(info_tablero.popleft())
    return tablero


def guardar_tablero(nombre_archivo: str, tablero: list) -> None:
    """
    esta funcion recibe el tablero de juego y un nombre de archivo (extension incluida), no retorna
    nada pero crea un archivo en el directorio relativo Archivos/ con el sufijo '_sol'
    antes de la extension
    """
    dir_archivo = os.path.join('Archivos', nombre_archivo)
    with open(dir_archivo, 'w') as archivo_sol:
        tablero_size = str(len(tablero))
        data_list = [tablero_size]
        for row in tablero:
            for entry in row:
                data_list.append(entry)
        print(','.join(data_list), file=archivo_sol)


def verificar_valor_bombas(tablero: list) -> int:
    """
    esta funcion verfica si el valor de las bombas en el tablero es valido, o sea si se encuentra
    entre 2 y 2n - 1 con n siendo la dimension de la matriz (tablero), recible el tablero de juego
    retorna la cantidad de bombas invalidas
    """
    max_size = 2 * len(tablero) - 1
    invalid = 0
    for row in tablero:
        for entry in row:
            if entry.isnumeric():
                if not 2 <= int(entry) <= max_size:
                    invalid += 1
    return invalid


def verificar_alcance_bomba(tablero: list, coordenada: tuple) -> int:
    """
    verifica que rango esta cubriendo una bomba, o sea, la cantidad de
    bloques que tapa su explosion, usa la funcion 'contar_bloques'
    retorna el rango de la bomba en forma de int
    """
    coord_x = coordenada[0]
    coord_y = coordenada[1]
    if tablero[coord_x][coord_y].isnumeric():
        fila_tablero = tablero[coord_x]
        col_tablero = list()
        for index in range(len(tablero)):
            col_tablero.append(tablero[index][coord_y])
        bloques_fila = contar_bloques(coord_y, fila_tablero)
        bloques_col = contar_bloques(coord_x, col_tablero)
        return bloques_fila + bloques_col + 1
    else:
        return 0


def regla_1(tablero: list) -> bool:
    """
    verifica si se cumple la regla 1, retorna True si es que se cumple, False en cualquier otro caso
    """
    final = True
    for row in range(len(tablero)):
        for col in range(len(tablero)):
            if tablero[row][col].isnumeric():
                if int(tablero[row][col]) != verificar_alcance_bomba(tablero, (row, col)):
                    final = False
    return final


def regla_3(tablero: list) -> bool:
    """
    verificas si se cumple la regla 3, retorna True si es que se cumple, False en otro caso
    """
    final = True
    for row in range(len(tablero)):
        for col in range(len(tablero)):
            if 'T' in tablero[row][col] and len(tablero[row][col]) > 1:
                final = False
    return final


def verificar_una_celda(tablero: list, coord: tuple) -> bool:
    """
    verifica si las celdas arriba, abajo o a los lados de una celda en especifico son iguales,
    retorna True si no la rodea ninguna igual, False si es que si
    """
    up = check_up(tablero, coord[0], coord[1])
    down = check_down(tablero, coord[0], coord[1])
    left = check_left(tablero, coord[0], coord[1])
    right = check_right(tablero, coord[0], coord[1])
    answers = [up, down, left, right]
    if True in answers:
        return False
    return True


def verificar_tortugas(tablero: list) -> int:
    """
    verifica la cantidad de tortugas invalidas en el tablero, o sea, tortugas directamente arriba, a
    bajo o a los lados de otra tortuga, recibe el tablero de juego
    y retorna la cantidad de tortugas invalidas
    """
    invalid = 0
    for row_num in range(len(tablero)):
        for col_num in range(len(tablero)):
            if tablero[row_num][col_num] == 'T':
                answer = verificar_una_celda(tablero, (row_num, col_num))
                if answer is False:
                    invalid += 1
    return invalid


def completado(tablero: list) -> bool:
    """
    esta funcion determina si se estan cumpliendo las 4 reglas, retorna True si es que
    se cumplen, False para otro caso
    """
    regla_1_l = regla_1(tablero)
    regla_2 = verificar_valor_bombas(tablero)
    regla_3_l = regla_3(tablero)
    regla_4 = verificar_tortugas(tablero)
    if [regla_1_l, regla_2, regla_3_l, regla_4] == [True, 0, True, 0]:
        return True
    return False


def coordenadas(tablero: list) -> list:
    """
    retorna las coordenadas (en tuplas de la forma (num row, num col))
    en una lista de todas las bombas del tablero
    """
    coords = []
    for row in range(len(tablero)):
        for col in range(len(tablero)):
            if tablero[row][col].isnumeric():
                coords.append((row, col))
    return coords


def is_inside(tablero: list, posicion: tuple) -> bool:
    """
    verifica si una posicion esta dentro o fuera de un tablero, retorna False
    si es que esta afuera, True si es que esta adentro
    """
    if posicion[0] < 0 or posicion[0] >= len(tablero):
        return False
    if posicion[1] < 0 or posicion[1] >= len(tablero[0]):
        return False
    return True


def validar_rangos(tablero: list, coord: tuple, coord_list: list) -> bool:
    """
    revisa como afecta el ingreso de una tortuga a los rangos de las bombas en
    la columna y fila afectada, retorna True si es que los rangos se mantienen
    mayores o iguales al numero de las bombas, False si alguna bomba queda
    con menos rango de lo que deberia
    """
    new_tablero = [[item for item in tablero[i]] for i in range(len(tablero))]
    new_tablero[coord[0]][coord[1]] = 'T'
    for entry in coord_list:
        if entry[0] == coord[0]:
            if verificar_alcance_bomba(tablero, entry) < int(tablero[entry[0]][entry[1]]):
                return False
        if entry[1] == coord[1]:
            if verificar_alcance_bomba(tablero, entry) < int(tablero[entry[0]][entry[1]]):
                return False
    return True


def validar_poner_tor(tablero: list, coord: tuple, coord_list: list) -> bool:
    """
    esta funcion verifica si es posible poner una tortuga en una celda especifica, basandose en las
    reglas definidas anteriormente.
    Retorna True si es posible poner la tortuga, False en otro caso
    """
    if is_inside(tablero, coord) is False:
        return False
    if tablero[coord[0]][coord[1]].isnumeric() or tablero[coord[0]][coord[1]] == 'T':
        return False
    if verificar_una_celda(tablero, coord) is False:
        return False
    if validar_rangos(tablero, coord, coord_list) is False:
        return False
    return True


def solucionar_tablero(tablero: list) -> list:
    """
    esta funcion soluciona el tablero mediante un algoritmo de backtracking ,
    retorna el tablero (lista de listas) resuelto con tortugas en lugares correctos
    """
    if completado(tablero) is True:
        return tablero
    bomb_coord_list = coordenadas(tablero)
    for row in range(len(tablero)):
        for col in range(len(tablero)):
            if tablero[row][col] == '-':
                if validar_poner_tor(tablero, (row, col), bomb_coord_list):
                    tablero[row][col] = 'T'
                    sol = solucionar_tablero(tablero)
                    if sol is not None:
                        return sol
                    tablero[row][col] = '-'
