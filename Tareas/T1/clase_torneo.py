from clases_arenas import ArenaMagnetica, ArenaMojada, ArenaNormal, ArenaRocosa
from clases_excavador import ExcavadorDocencio, ExcavadorHibrido, ExcavadorTareo
import parametros
from random import sample, choices, choice
from funciones import (
    diccionario_arenas_disponibles, diccionario_excavadores_disponibles, len_excavador_mas_largo,
    len_descripcion_mas_larga, len_nombre_mas_largo)
import manejo_archivos


class Torneo():

    def __init__(self):
        self.eventos = parametros.EVENTOS_POSIBLES
        self.equipo = []  # aqui se agregan los excavadores que se van a crear durante el init
        self.mochila = []  # aqui se van a ir agregando los items encontrados
        self._metros_cavados = 0.0
        self._meta = parametros.METROS_META
        self._dias_transcurridos = 1  # lo entiendo mas como un dia actual
        self._dias_totales = parametros.DIAS_TOTALES_TORNEO
        self._arenas_totales = []
        self._excavadores_totales = []
        self._finalizado = False

        # aca instancio cada arena con sus clases respectivas y las agrego al
        # atributo correspondiente, instancio arena inicial

        clases = {
                'normal': ArenaNormal,
                'rocosa': ArenaRocosa,
                'mojada': ArenaMojada,
                'magnetica': ArenaMagnetica
            }

        for entry in manejo_archivos.lista_arenas:
            self._arenas_totales.append(clases[entry.type](*entry))

        # aqui va ARENA_INICIAL instanciada como la arena correspondiente
        self._arena = clases[manejo_archivos.arena_inicial.type](*manejo_archivos.arena_inicial)

        # instancio cada trabajador usando la clase correspondiente y
        # los acumulo en __excavadores totales
        for entry in manejo_archivos.lista_excavadores:
            name = entry.name
            if entry.type == 'docencio':
                self._excavadores_totales.append(ExcavadorDocencio(self.arena, name, *entry[2:]))
            if entry.type == 'tareo':
                self._excavadores_totales.append(ExcavadorTareo(self.arena, name, *entry[2:]))
            if entry.type == 'hibrido':
                self._excavadores_totales.append(ExcavadorHibrido(self.arena, name, *entry[2:]))

        # instancio el equipo inicial siendo este una poblacion al azar con tamaño igual a
        # a CANTIDAD_EXCAVADORES_INICIALES y los elimino de la poblacion general
        self.equipo = sample(self._excavadores_totales, parametros.CANTIDAD_EXCAVADORES_INICIALES)
        for entry in self.equipo:
            self._excavadores_totales.remove(entry)

    # defino properties correspondientes

    @property
    def meta(self):
        return self._meta

    @property
    def dias_totales(self):
        return self._dias_totales

    @property
    def dias_transcurridos(self):
        return self._dias_transcurridos

    @dias_transcurridos.setter
    def dias_transcurridos(self, new):
        if new > self._dias_totales:
            self._dias_transcurridos = self._dias_totales
        else:
            self._dias_transcurridos = new

    @property
    def metros_cavados(self):
        return self._metros_cavados

    @metros_cavados.setter
    def metros_cavados(self, new):
        if new < 0.0:
            self._metros_cavados = 0.0
        else:
            self._metros_cavados = round(new, 2)

    @property
    def arena(self):
        return self._arena

    @arena.setter     # cambia arena del torneo y la arena de cada excavador
    def arena(self, new):
        '''
        settea la nueva arena, devolviendo la anterior a arenas totales
        ademas cambia el valor de arena de cada excavador en el equipo y
        en la poblacion general,
        para hacer esto llama al setter de la clase Excavador (y sus heredadas)
        '''
        self._arenas_totales.append(self._arena)
        self._arena = new
        for worker in self.equipo:
            # se llama al setter de la clase Excavador y sus heredadas
            # este le cambia la arena al trabajador y define su probabilidad de encontrar
            # item segun corresponda en la arena (clases_excavador.py, line 96 to 106)
            worker.arena = new

    @property
    def arenas_totales(self):
        return self._arenas_totales

    def iniciar_evento(self):
        '''
        determina si inicia o no un evento, y que evento es

        retorna None, modifica self.arena si ocurre un evento
        '''
        # defino los pesos para que ocurra un evento
        pesos_evento = [parametros.PROB_INICIAR_EVENTO, 1 - parametros.PROB_INICIAR_EVENTO]
        # llevo acabo la probabilidad para ver si ocurre uno
        eleccion = choices(('si', 'no'), pesos_evento, k=1)
        if eleccion[0] == 'no':
            print(' >> *vine boom sound* No ocurrio nada, anticlimatico :/')
            print(' >> La arena se mantiene igual ;]')
        else:
            # le descuento la felicidad a cada trabajador en el equipo
            print(f' >> Felicidad perdida = -{parametros.FELICIDAD_PERDIDA}')
            for worker in self.equipo:
                worker.felicidad -= parametros.FELICIDAD_PERDIDA

            # hago un dict con las arenas divididas por tipo y devuelvo la actual a las totales
            # la utilidad de esto es para poder elegir una arena al azar cuando ocurra un
            # evento que lo cambia y evitar elegir la misma
            arenas_disponibles = diccionario_arenas_disponibles(
                self._arenas_totales, ArenaNormal, ArenaMojada, ArenaRocosa, ArenaMagnetica)

            # determino que tipo de evento ocurre
            pesos_si = [parametros.PROB_LLUVIA, parametros.PROB_TERREMOTO, parametros.PROB_DERRUMBE]
            evento_final = choices(self.eventos, pesos_si, k=1)

            if evento_final[0] == 'derrumbe':
                print(' >> NOPUEDESER, OCURRIO UN DERRUMBE')
                print(' >> Wow, la arena ahora es normal')
                # elijo arena normal al azar, la asigno al atributo y la elimino de las totales
                new_arena = choice(arenas_disponibles['normal'])
                # esto ademas de cambiar el atributo a torneo se la cambia a cada excavador
                self.arena = new_arena
                self._arenas_totales.remove(new_arena)
                self.metros_cavados -= parametros.METROS_PERDIDOS_DERRUMBE

            if evento_final[0] == 'lluvia':
                print(' >> SALVENSE ESTA LLOVIENDOOOOOOO *se ahoga*')
                if type(self.arena) == ArenaNormal:
                    print(' >> Wow, la arena ahora esta mojada')
                    new_arena = choice(arenas_disponibles['mojada'])
                    self.arena = new_arena
                    self._arenas_totales.remove(new_arena)

                elif type(self.arena) == ArenaRocosa:
                    print(' >> Que es lo que pasa realmente?, la arena ahora es magnetica')
                    new_arena = choice(arenas_disponibles['magnetica'])
                    self.arena = new_arena
                    self._arenas_totales.remove(new_arena)

                else:
                    print(' >> Que fome, la arena no cambia >=[')

            if evento_final[0] == 'terremoto':
                print(' >> ESTA TEMBLANDO AAAAAAAA *flashbacks del 2010* *se mea* *se sonroja*')
                if type(self.arena) == ArenaNormal:
                    print(' >> Como Dwayne, la arena ahora es rocosa (q chistoso)')
                    new_arena = choice(arenas_disponibles['rocosa'])
                    self.arena = new_arena
                    self._arenas_totales.remove(new_arena)

                elif type(self.arena) == ArenaMojada:
                    print(' >> Que es lo que pasa realmente?, la arena ahora es magnetica')
                    new_arena = choice(arenas_disponibles['magnetica'])
                    self.arena = new_arena
                    self._arenas_totales.remove(new_arena)

                else:
                    print(' >> Que fome, la arena no cambia >=[')

    def simular_dia(self) -> None:
        """
        lleva acabo la simulacion de un dia de torneo, sigue este orden
        1. si la arena es magnetica cambia sus atributos segun lo pedido
        2. cada excavador no descansando excava
        3. revisa que items se encuentran
        4. revisa ocurrencia de eventos
        5. termina el dia y los excavadores con 0 energia descansan,

        si se simula dia cuando ya se llego al ultimo dia del torneo, printea
        los resultados
        no tiene return
        """
        # reviso si la arena actual es magnetica. si asi es, cambio sus atributos
        if type(self.arena) == ArenaMagnetica:
            self.arena.cambiar_atributo_nuevo_dia()
        print()
        print('{:^50}'.format(f'Dia {self._dias_transcurridos}'))
        print('-' * 50)

        # se llama la funcion cavar para excavadores no descansando
        print('Fase 1: Excavacion de hoyo >=]\n---\n')
        metros_cavados_este_dia = 0
        for worker in self.equipo:
            if worker.dias_para_descansar == 0:
                metros_cavados_por_trabajador = worker.cavar()
                # la funcion de la linea de abajo calcula el gasto energetico
                # y se lo resta al directamente al atribto
                worker.gastar_energia()
                metros_cavados_este_dia += metros_cavados_por_trabajador
                print(f' >> {worker.nombre} cavo {metros_cavados_por_trabajador} metros!1!! :O')
            else:
                print(f' >> {worker.nombre} es un flojo y esta descansando >=(')
        print(f'\n > SUGOI, el equipo logro cavar {round(metros_cavados_este_dia, 2)} metros!!')
        self.metros_cavados += round(metros_cavados_este_dia, 2)

        input('\nPresiona cualquier tecla para continuar a la proxima fase ')

        # las siguientes lineas determinan que items se van a encontrar
        print('-' * 50)
        print('Fase 2: Aparicion de Items! :D\n---\n')
        cant_cons = 0
        cant_tesoros = 0
        for worker in self.equipo:
            nombre = worker.nombre
            if worker.dias_para_descansar > 0:
                print(f' >> {nombre} esta descansando, no puede buscar items que no sea patudo')
            else:
                item_final = worker.encontrar_item()
                if item_final is None:
                    print(f' >> {nombre} no encontro nada :c, que bobe')
                else:
                    self.mochila.append(item_final)
                    if item_final.tipo == 'consumible':
                        cant_cons += 1
                        print(f' >> SIUU, {nombre} encontro el consumible: {item_final.nombre}')
                    elif item_final.tipo == 'tesoro':
                        cant_tesoros += 1
                        print(f' >> WUJUU!, {nombre} encontro el tesoro: {item_final.nombre}')
        print(f'\n > Bkn, el equipo encontro {cant_cons} consumibles y {cant_tesoros} tesoros')
        print(f' > Lo que hace un total de {cant_cons + cant_tesoros} items, gran orgullo :3')
        input('\nPresiona cualquier tecla para continuar a la proxima fase ')

        # las siguientes lineas determinan eventos
        print('-' * 50)
        print('Fase 3: La hora de los eventos! o.o\n---\n')
        self.iniciar_evento()
        print()

        print('-' * 50)
        print('Ha llegado el fin del dia... zzzzzzzzzz\n---\n')
        for worker in self.equipo:
            worker.dias_para_descansar -= 1
            if worker.dias_para_descansar == 0 and worker.energia == 0:
                worker.descansar()
                print(f' >> {worker.nombre} descansara por {worker.dias_para_descansar} dias')
        # reviso si se cumplio el ultimo dia del torneo
        if self.dias_transcurridos == self.dias_totales:
            print('\n DING DING DING DING, HA FINALIZADO EL TORNEO')
            self._finalizado = True
        self.dias_transcurridos += 1

    def usar_consumible(self, consumible):
        '''
        esta funcion aplica los efectos de un consumible a todos los trabajadores
        en el equipo actual, usa el metodo consumir de cada uno,
        elimina el consumible de la mochila, no tiene return
        '''
        print('\n >> Se va a usar un consumible!!!!')
        print(f' >> Sus efectos son {consumible.descripcion}!!!')
        for worker in self.equipo:
            if worker.dias_para_descansar == 0:
                worker.consumir(consumible)
            else:
                print(f' >> {worker.nombre} no puede usar el consumible, esta descansando')
        self.mochila.remove(consumible)

    def abrir_tesoro(self, tesoro):
        '''
        esta funcion usa el tesoro entregado y aplica sus efectos sobre el torneo,
        si el tesoro es calidad 1, agrega un trabajador del tipo correspondiente
        si el tesoro es calidad 2, cambia la arena al tipo correspondinte
        '''
        diccionario_arenas_libres = diccionario_arenas_disponibles(
            self._arenas_totales, ArenaNormal, ArenaMojada, ArenaRocosa, ArenaMagnetica)
        diccionario_excavadores_libres = diccionario_excavadores_disponibles(
            self._excavadores_totales, ExcavadorDocencio, ExcavadorTareo, ExcavadorHibrido)
        print('\n >> Se va a abrir un tesoro!!!1')
        print(f' >> Sus efectos son "{tesoro.descripcion}"!!!')
        if tesoro.calidad == 1:
            # eligo excavador al azar de los disponibles, elimino de poblacion original
            # y agrego al equipo
            if len(self._excavadores_totales) == 0:
                print(' >> No quedan excavadores disponibles para agregar :c')
            else:
                excavador_nuevo = choice(diccionario_excavadores_libres[tesoro.cambio])
                print(f' >> {excavador_nuevo.nombre} se ha unido al equipo!!!!!')
                self._excavadores_totales.remove(excavador_nuevo)
                excavador_nuevo.arena = self._arena
                self.equipo.append(excavador_nuevo)

        else:
            # eligo arena al azar del tipo entregado, retorno la ya existente a la pobl. original
            # y setteo la arena nueva
            arena_nueva = choice(diccionario_arenas_libres[tesoro.cambio])
            print(f' >> WTF, la arena ahora es de tipo {tesoro.cambio}')
            self._arenas_totales.remove(arena_nueva)
            self.arena = arena_nueva
        self.mochila.remove(tesoro)

    def mostrar_estado(self):
        '''
        muestra el estado del torneo en el dia actual
        '''
        longest_name = len_excavador_mas_largo(self.equipo)
        max_width = 60 + longest_name
        string = f'''
        {'* Estado del Torneo *' : ^{max_width}}
        {'-' * max_width}
        Dia actual: {self.dias_transcurridos} / {self.dias_totales}
        Tamaño del equipo: {len(self.equipo)}
        Tipo de arena: {self.arena.tipo}
        Metros cavados: {self.metros_cavados} / {self.meta}
        {'-' * max_width}
        {'Equipo actual' : ^{max_width}}
        {'-' * max_width}
        {'Nombre': ^{longest_name}}|{'Tipo': ^11}|{'Energia': ^11}|{'Fuerza': ^11}|{'Suerte': ^11}|{'Felicidad': ^11}
        {'-' * max_width}'''
        # si bien en la linea superior sobrepaso los limites de caracteres por linea, se deja asi
        # debido a que editarlo de cualquier otra manera haria mas dificil de leer el codigo
        # como dice la guia pep8 de python "know when to be inconsistent"
        print(f'{string.ljust(max_width)}')
        for entry in self.equipo:
            nombre = f'{entry.nombre: ^{longest_name}}|'
            tipo = f'{entry.tipo: ^11}|'
            energia = f'{entry.energia: ^11}|'
            fuerza = f'{entry.fuerza: ^11}|'
            suerte = f'{entry.suerte: ^11}|'
            felicidad = f'{entry.felicidad: ^11}'
            print(f'''        {nombre + tipo + energia + fuerza + suerte + felicidad}''')
        print()

    def mostrar_mochila(self):
        '''
        muestra los items en la mochila, retorna la opcion elegida para que despues
        sea utilizada en el menu manager
        '''
        if len(self.mochila) == 0:
            print('\n >> La mochila no tiene ningun item :c, volviendo al menu anterior')
            return 'r'
        else:
            longest_name = len_nombre_mas_largo(self.mochila)
            longest_desc = len_descripcion_mas_larga(self.mochila)
            max_width = 18 + longest_name + longest_desc
            string = f'''
            {'* MOCHILA *' : ^{max_width}}
            {'-' * max_width}
            {'Nombre': ^{longest_name + 2}}|{'Tipo' : ^12}|{'Descripcion': ^{longest_desc + 2}}
            {'-' * max_width}'''
            print(string)
            for i in range(len(self.mochila)):
                nombre = f'{self.mochila[i].nombre: ^{longest_name + 2}}'
                tipo = f'{self.mochila[i].tipo: ^12}'
                desc = f'{self.mochila[i].descripcion: ^{longest_desc + 2}}'
                print(f'       [{i + 1}]  {nombre}|{tipo}|{desc}')
            print(f'''            {'-' * max_width}''')
            print('''        [r] Volver\n        [x] Finalizar programa\n''')
            answer = input('Que deseas hacer (numero de item, r o x): ')
            if answer.isdigit() and int(answer) <= len(self.mochila):
                return int(answer)
            elif answer == 'r':
                return 'r'
            elif answer == 'x':
                return 'x'
            else:
                print('\n >> Opcion invalida, elige denuevo')
