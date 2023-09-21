# en este archivo esta escrito el codigo que se encarga de hacer cada menu
from clase_torneo import Torneo
from funciones import guardar_partida, menu_partidas_guardadas
from carga_partidas import cargar_partida
import os
from parametros import PATH_GUARDAR_CARGAR

VOLVER = "volver"
SALIR = "salir"


def menu_inicio(torneo):
    while True:
        print(f"""
        {'*  MENU DE INICIO *' : ^25}
        -------------------------
        [1] Iniciar nueva partida
        [2] Cargar partida antigua
        [x] Finalizar programa
        """)
        resp = input(" >> ¿Que opcion deseas elegir? (1, 2 o x): ")

        if resp == "1":
            return "ir_menu_principal"

        elif resp == "2":
            return "ir_menu_partidas"

        elif resp == "x":
            return SALIR

        else:
            print('\n > Por favor entrega una opcion valida')


def menu_principal(torneo: Torneo):
    while True:
        print(f"""
        {'*  MENU PRINCIPAL *' : ^25}
        -------------------------
        [1] Simular un dia de torneo
        [2] Mostrar estado del torneo
        [3] Ver mochila
        [4] Guardar partida
        [r] Volver atras
        [x] Finalizar programa
        """)
        resp = input("¿Qué quieres hacer? (1, 2, 3, 4, r o x): ")
        if resp == "1":

            if torneo._finalizado is True:
                print()
                print(f' > Fin del torneo!, el equipo logro cavar {torneo.metros_cavados} metros!')
                print(f' > La meta a alcanzar era de {torneo.meta} metros! :o')
                if torneo.metros_cavados < torneo.meta:
                    print(' > Lamentablemente hoy la victoria se la lleva el malvado Dr Pinto :c')
                elif torneo.metros_cavados > torneo.meta:
                    print(' > EL MALVADO DR PINTO HA SIDO DERROTADO!!!!!!!')
                else:
                    print(' > Esto es interesante, tenemos un empate??????')
                input('\nPresiona cualquier tecla para volver al menu de inicio ')
                return 'ir_menu_inicio'

            else:
                torneo.simular_dia()
                input('\nPresiona cualquier tecla para volver al menu principal ')

        elif resp == "2":
            torneo.mostrar_estado()
            input('\nPresiona cualquier tecla para volver al menu principal ')

        elif resp == '3':
            return 'ir_menu_mochila'

        elif resp == '4':
            name = input('\nQue nombre quieres usar?(solo usar letras, sin extension) ')
            if name.isalpha() is True:
                name += '.txt'
                guardar_partida(torneo, name)
                print('\n >> Se ha guardado la partida! ')
            else:
                print('\n >> Nombre invalido, volviendo al menu principal')

        elif resp == "r":
            return VOLVER

        elif resp == "x":
            return SALIR

        else:
            print('\n > Por favor elegir un valor valido n.n')


def mostrar_mochila(torneo: Torneo):
    while True:
        resp = torneo.mostrar_mochila()
        if type(resp) == int:
            if torneo._finalizado is True:
                print('\n > Nao nao, no puede ocupar item, el torneo termino')
            else:
                item_a_usar = torneo.mochila[resp - 1]
                if item_a_usar.tipo == 'consumible':
                    torneo.usar_consumible(item_a_usar)
                elif item_a_usar.tipo == 'tesoro':
                    torneo.abrir_tesoro(item_a_usar)

        elif resp == "r":
            return VOLVER

        elif resp == "x":
            return SALIR


def mostrar_menu_partidas(torneo: Torneo):
    while True:
        archivos_guardados = os.listdir(os.path.join(PATH_GUARDAR_CARGAR))
        resp = menu_partidas_guardadas(archivos_guardados)
        if type(resp) == int:
            partida_a_cargar = archivos_guardados[resp - 1]
            # cargar partida recibe el nombre con la extension, por eso no se lo quito
            # a partida_a_cargar
            cargar_partida(torneo, partida_a_cargar)
            return 'ir_menu_principal'

        elif resp == "r":
            return VOLVER

        elif resp == "x":
            return SALIR


def menu_manager(torneo: Torneo):
    historial = ["ir_menu_inicio"]
    respuesta = ""
    while respuesta != SALIR:
        estado_actual = historial[-1]

        if estado_actual == "ir_menu_inicio":
            if torneo._finalizado is True:
                torneo = Torneo()
            respuesta = menu_inicio(torneo)

        elif estado_actual == "ir_menu_principal":
            respuesta = menu_principal(torneo)

        elif estado_actual == "ir_menu_mochila":
            respuesta = mostrar_mochila(torneo)

        elif estado_actual == 'ir_menu_partidas':
            respuesta = mostrar_menu_partidas(torneo)

        if respuesta == VOLVER:
            historial.pop()

        elif respuesta.startswith("ir"):
            historial.append(respuesta)


t = Torneo()
menu_manager(t)
