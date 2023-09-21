from parametros import PATH_GUARDAR_CARGAR
import os
'''
funciones de usos varios para hacer mas legible codigo en los otros archivos
'''


def mantener_entre_extremos(min: int, max: int, new_val: int) -> int:
    '''
    esta funcion retorna un valor limitado a los valores maximos y minimos, si el numero
    es mayor al maximo retorna el maximo, si es menor al minimo retorna el minimo
    si esta entremedio retorna el valor entregado
    '''
    if new_val >= max:
        return max
    elif new_val <= min:
        return min
    else:
        return new_val


def reducir_dia(dia_actual: int, new: int) -> int:
    '''
    Recibe la cantidad de dias que le faltan por descansar a un excavador
    si solo le queda un dia, retorna un tupla (0, 100) donde 0 representa
    que no le quedan dias por descansar y 100 representa que la energia aumenta
    a ese valor maximo.
    Si el valor nuevo es menor o igual que 0, retorna 0,
    en otro caso retorna el valor nuevo
    '''
    if dia_actual >= 0 and new == 0:
        return 0, 100
    elif new <= 0:
        return 0
    else:
        return new


def diccionario_arenas_disponibles(
        arenas_totales: list, arena_normal: object, arena_mojada: object,
        arena_rocosa: object, arena_magnetica: object) -> dict:
    '''
    recibe una lista de todas las arenas totales, retorna un
    diccionario del tipo

    {
        "normal" : [lista_de_arenas_de_ese_tipo]
        "rocosa" : [lista_de_arenas_de_ese_tipo]
        "magnetica" : [lista_de_arenas_de_ese_tipo]
        "mojada" : [lista_de_arenas_de_ese_tipo]

        }
    '''
    norm = [entry for entry in arenas_totales if type(entry) == arena_normal]
    wet = [entry for entry in arenas_totales if type(entry) == arena_mojada]
    magn = [entry for entry in arenas_totales if type(entry) == arena_magnetica]
    rock = [entry for entry in arenas_totales if type(entry) == arena_rocosa]

    dictionary = {
        'normal': norm,
        'rocosa': rock,
        'magnetica': magn,
        'mojada': wet
    }

    return dictionary


def diccionario_excavadores_disponibles(
        excavadores_totales: list, docencio: object, tareo: object, hibrido: object) -> dict:
    '''
    recibe una lista de todos los excavadores disponibles que no esten en un equipo
    retorna un diccionario de la forma

    {
    'docencio': [lista de excavadores docencios]
    'tareo': [lista de excavadores tareos]
    'hibrido': [lista de excavadores hibridos]
    }
    '''
    docencio = [entry for entry in excavadores_totales if type(entry) == docencio]
    tareo = [entry for entry in excavadores_totales if type(entry) == tareo]
    hibrido = [entry for entry in excavadores_totales if type(entry) == hibrido]

    dictionary = {
        'docencio': docencio,
        'tareo': tareo,
        'hibrido': hibrido
    }
    return dictionary


def len_nombre_mas_largo(lista_de_items: list) -> int:
    '''
    retorna la longitud del nombre mas largo en los items
    '''
    maximum = 0
    for entry in lista_de_items:
        if len(entry.nombre) > maximum:
            maximum = len(entry.nombre)
    return maximum


def len_descripcion_mas_larga(lista_de_items: list) -> int:
    '''
    retorna la longitud de la descripcion mas larga en los items
    '''
    maximum = 0
    for entry in lista_de_items:
        if len(entry.descripcion) > maximum:
            maximum = len(entry.descripcion)
    return maximum


def len_excavador_mas_largo(equipo: list) -> int:
    '''
    retorna la longitud del nombre mas largo en los excavadores activos
    '''
    maximum = 0
    for entry in equipo:
        if len(entry.nombre) > maximum:
            maximum = len(entry.nombre)
    if maximum == 0:
        return 11
    else:
        return maximum


def guardar_partida(torneo: object, nombre) -> None:
    with open(os.path.join(PATH_GUARDAR_CARGAR, nombre), 'w', encoding='UTF-8') as archivo_datos:

        print('datos arena actual', file=archivo_datos)
        print('nombre,items', file=archivo_datos)
        arena_name = torneo.arena.nombre
        item_names = '.'.join([entry.nombre for entry in torneo.arena.items])
        print(arena_name + ',' + item_names, file=archivo_datos)

        print('datos todas arenas', file=archivo_datos)
        print('nombre,items', file=archivo_datos)
        for arena in torneo.arenas_totales:
            gen_arena_name = arena.nombre
            gen_item_names = '.'.join([entry.nombre for entry in arena.items])
            print(gen_arena_name + ',' + gen_item_names, file=archivo_datos)

        print('datos equipo', file=archivo_datos)
        print(
            'nombre,edad,energ,fuerza,suerte,felicidad,dias_rest,arena,prob', file=archivo_datos)
        for excavador in torneo.equipo:
            data_dict = excavador.__dict__
            attribute_values = [str(value) for value in data_dict.values()]
            attribute_values[7] = arena_name
            print(','.join(attribute_values), file=archivo_datos)

        print('datos mochila', file=archivo_datos)
        mochila_content = ','.join([item.nombre for item in torneo.mochila])
        print(mochila_content, file=archivo_datos)

        print('datos torneo', file=archivo_datos)
        print('metros cavados,dias transcurridos, finalizado', file=archivo_datos)
        metros_cavados = str(torneo.metros_cavados)
        dias_transcurridos = str(torneo.dias_transcurridos)
        finalizado = str(torneo._finalizado)
        tourney_str = ','.join([metros_cavados, dias_transcurridos, finalizado])
        print(tourney_str, file=archivo_datos)


def menu_partidas_guardadas(archivos_disponibles):
    '''
    muestra todos los archivos disponibles para cargar partidas, retorna la respuesta,
    el indice del archivo + 1 o un comando para volver en los menus
    '''
    if len(archivos_disponibles) == 0:
        print('\n >> No hay archivos guardados :c')
        return 'r'
    else:
        longest_name = max([len(entry) for entry in archivos_disponibles])
        max_width = longest_name + 2
        string = f'''
        {'* PARTIDAS *' : ^{max_width}}
        {'-' * max_width}'''
        print(string)
        for i in range(len(archivos_disponibles)):
            nombre = f'{archivos_disponibles[i]: ^{max_width}}'
            print(f'    [{i + 1}] {nombre}')
        print(f'''        {'-' * max_width}''')
        print('''    [r] Volver\n    [x] Finalizar programa\n''')
        answer = input('Que deseas hacer (numero de archivo, r o x): ')
        if answer.isdigit() and int(answer) <= len(archivos_disponibles):
            return int(answer)
        elif answer == 'r':
            return 'r'
        elif answer == 'x':
            return 'x'
        else:
            print('\n >> Opcion invalida, elige denuevo')
