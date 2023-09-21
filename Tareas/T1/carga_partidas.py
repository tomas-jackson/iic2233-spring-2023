import manejo_archivos
from parametros import PATH_GUARDAR_CARGAR
from clase_torneo import Torneo, ExcavadorDocencio, ExcavadorHibrido, ExcavadorTareo
from clases_items import Consumibles, Tesoros
from clases_arenas import ArenaMagnetica, ArenaMojada, ArenaNormal, ArenaRocosa
import os.path

# instancio todo en su estado 'default' para poder usar al cargar partida
arenas_totales = []
excavadores_totales = []
items_totales = []

clases = {
        'normal': ArenaNormal,
        'rocosa': ArenaRocosa,
        'mojada': ArenaMojada,
        'magnetica': ArenaMagnetica
    }

for entry in manejo_archivos.lista_arenas:
    arenas_totales.append(clases[entry.type](*entry))

arena_inicial = clases[manejo_archivos.arena_inicial.type](*manejo_archivos.arena_inicial)

arenas_totales.append(arena_inicial)


for entry in manejo_archivos.lista_excavadores:
    if entry.type == 'docencio':
        excavadores_totales.append(ExcavadorDocencio(arena_inicial, entry.name, *entry[2:]))
    if entry.type == 'tareo':
        excavadores_totales.append(ExcavadorTareo(arena_inicial, entry.name, *entry[2:]))
    if entry.type == 'hibrido':
        excavadores_totales.append(ExcavadorHibrido(arena_inicial, entry.name, *entry[2:]))

for entry in manejo_archivos.lista_tesoros:
    items_totales.append(Tesoros(entry.name, 'tesoro', entry.descripcion, *entry[2:]))
for entry in manejo_archivos.lista_consumibles:
    items_totales.append(Consumibles(entry.name, 'consumible', *entry[1:]))


def cargar_partida(torneo: Torneo, nombre_archivo):
    with open(os.path.join(PATH_GUARDAR_CARGAR, nombre_archivo), 'r', encoding='UTF-8') as archivo:
        # empiezo a extraer la informacion
        informacion = [entry.strip() for entry in archivo.readlines()]
        # determino la info de la arena actual
        info_arena_actual = informacion[2].split(',')
        info_arena_actual[1] = info_arena_actual[1].split('.')
        # reviso las arenas totales para encontrar a la actual, asumo que no se repiten
        for entry in arenas_totales:
            if info_arena_actual[0] == entry.nombre:
                nueva_arena_actual = entry  # esta variable reemplaza torneo._arena
        # asumo que si es posible que se repita un item
        # itero sobre la lista de isntancias item, si el nombre de alguno
        # esta en la lita de nombres de la arena actual guardada lo almaceno
        # y finalmente redefino la variable de items de la arena actual
        items_nuevos = []
        for item in items_totales:
            if item.nombre in info_arena_actual[1]:
                items_nuevos.append(item)
        nueva_arena_actual.items = items_nuevos

        nuevas_arenas_disponibles = []  # esta variable reemplaza torneo._arenas_totales
        # encuentro hasta que linea se nos entrega informacion de las arenas disponibles
        for index in range(len(informacion)):
            if informacion[index] == 'datos equipo':
                fin_datos_arena = index
            if informacion[index] == 'datos mochila':
                fin_datos_equipo = index
        # cada linea la convierto en una lista para acceder facilmente a su informacion
        info_arenas_general = [entry.split(',') for entry in informacion[5:fin_datos_arena]]
        # cada linea de info_arenas_general es informacion de una arena, itero sobre esa lista
        # hago split de la segunda entrada para acceder facilmente a los nombres de los items
        # que estan disponibles en esa arena
        for arena_info in info_arenas_general:
            arena_info[1] = arena_info[1].split('.')
            # con la informacion en el formato requerido, sigo el mismo proceso usado mas arriba
            # para determinar la info de la arena actual
            for entry in arenas_totales:
                if arena_info[0] == entry.nombre:
                    nueva_arena_general = entry
            items_nuevos = []
            for item in items_totales:
                if item.nombre in arena_info[1]:
                    items_nuevos.append(item)
            nueva_arena_general.items = items_nuevos
            nuevas_arenas_disponibles.append(nueva_arena_general)

        # ahora extraigo la informacion de los excavadores en el equipo, arreglo formato
        equipo_data = [
            entry.split(',') for entry in informacion[fin_datos_arena + 2:fin_datos_equipo]]
        new_team = []  # reemplaza torneo.equipo
        for excavador in excavadores_totales:
            for excavador_info in equipo_data:
                # si el nombre del excavador coincide con uno en la info del equipo
                # edito los valores del excavador a los que estan en el archivo
                # agrego el excavador al equipo nuevo, elimino los excavadores del total
                if excavador.nombre == excavador_info[0]:
                    excavador._edad = int(excavador_info[1])
                    excavador._energia = int(excavador_info[2])
                    excavador._fuerza = int(excavador_info[3])
                    excavador._suerte = int(excavador_info[4])
                    excavador._felicidad = int(excavador_info[5])
                    excavador._dias_para_descansar = int(excavador_info[6])
                    excavador._arena = nueva_arena_actual
                    excavador._prob_item = float(excavador_info[8])
                    new_team.append(excavador)
        # creo la nueva lista de excavadores disponibles, reemplaza torneo._excavadores_totales
        new_excavadores_general = [entry for entry in excavadores_totales if entry not in new_team]
        # determino items dentro de la mochila
        info_mochila = informacion[-4].split(',')
        new_mochila = []  # reemplaza torneo.mochila
        for item in items_totales:
            if item.nombre in info_mochila:
                for i in range(info_mochila.count(item.nombre)):
                    new_mochila.append(item)

        # finalmente determino los ultimos parametros del torneo
        datos_extra_torneo = informacion[-1].split(',')

        # para terminar cambio los atributos correspondientes del torneo, para 'cargar'
        torneo.equipo = new_team
        torneo.mochila = new_mochila
        torneo._metros_cavados = float(datos_extra_torneo[0])
        torneo._dias_transcurridos = int(datos_extra_torneo[1])
        torneo._arenas_totales = nuevas_arenas_disponibles
        torneo._excavadores_totales = new_excavadores_general
        if datos_extra_torneo[2] == 'False':
            torneo._finalizado = False
        else:
            torneo._finalizado = True
        torneo._arena = nueva_arena_actual
