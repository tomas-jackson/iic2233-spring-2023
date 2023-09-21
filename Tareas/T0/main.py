import tablero
import functions

# verificacion para menu de inicio
archivo_a_abrir = input('\n**MENU DE INICIO**\n\nQue archivo deseas abrir? (incluir extension): ')
directorio = functions.os.path.join('Archivos', archivo_a_abrir)

if not functions.os.path.exists(directorio):  # si el archivo no existe termina el codigo
    print('\nEl archivo no existe\nAdios :)\n')

else:  # si el archivo si existe el codigo principal es ejecutado
    executing = True
    tablero_juego = functions.cargar_tablero(archivo_a_abrir)
    while executing:
        print(functions.formar_menu_acciones())
        user_choice = input('\n>> Que deseas hacer? (ingrese numero de la opcion): ')
        if user_choice in ['1', '2', '3', '4']:  # bajo esta linea se corre el codigo principal

            if user_choice == '1':
                print()
                tablero.imprimir_tablero_con_utf8(tablero_juego)

            if user_choice == '2':
                tortugas_invalidas = functions.verificar_tortugas(tablero_juego)
                bombas_invalidas = functions.verificar_valor_bombas(tablero_juego)
                if tortugas_invalidas == bombas_invalidas and bombas_invalidas == 0:
                    print('\n---\n\n >> Todas las bombas y tortugas son validas!! :D\n\n---')
                else:
                    print('\n---\n\n >> No todos los elementos en el tablero son validos :c\n\n---')

            if user_choice == '3':
                solved_tablero = functions.solucionar_tablero(tablero_juego)
                if solved_tablero is not None:
                    print('\n---\n\n >> El tablero se ha solucionado :D\n\n---')
                    new_file_name = archivo_a_abrir.split('.')
                    nombre_archivo = new_file_name[0] + '_sol.' + new_file_name[1]
                    functions.guardar_tablero(nombre_archivo, tablero_juego)
                else:
                    print('\n---\n\n >> El tablero no tiene solucion\n\n---')

            if user_choice == '4':
                if functions.completado(tablero_juego):
                    print('\n---\n\n >> Yipieee, la solucion es valida n.n\n\n---')
                else:
                    print('\n---\n\n >> Que sad, la solucion no sirve :c\n\n---')

        elif user_choice == '0':
            executing = False
            print('\nGracias por tu trabajo protegiendo al DCCastillo, hasta la procsimaaaaaa\n')
        else:
            print('\n---\n\n>> Input invalido, favor elige de nuevo\n\n---')
