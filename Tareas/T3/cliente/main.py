from clientes import Cliente
from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_juego import VentanaJuego
import sys
from PyQt5.QtWidgets import QApplication


class Manager():

    def __init__(self, port) -> None:
        self.ventana_inicio = VentanaInicio()
        self.ventana_juego = VentanaJuego()
        self.cliente = Cliente(port)
        self.conexiones()
        self.metodos_iniciales()
        self.inicializar()

    def conexiones(self):

        self.cliente.senal_parametros.connect(self.ventana_inicio.actualizar_pixmaps_inicial)
        self.cliente.senal_cambiar_usuarios.connect(self.ventana_inicio.actualizar_usuarios)
        self.cliente.senal_popup_full.connect(self.ventana_inicio.abrir_popup_full)
        self.cliente.senal_spot_open.connect(self.ventana_inicio.abrir_popup_spot_found)
        self.cliente.senal_ingame.connect(self.ventana_inicio.abrir_popup_ingame)
        self.cliente.senal_dead_server.connect(self.ventana_inicio.popup_dead_server)

        self.ventana_inicio.senal_cerrado.connect(self.cliente.enviar_info)
        self.ventana_inicio.senal_inicio.connect(self.cliente.enviar_info)

        self.cliente.senal_start_round.connect(self.ventana_juego.recibir_info_round)
        self.cliente.senal_start_round.connect(self.abrir_ventana_juego)
        self.cliente.senal_botones_jugar_si.connect(self.ventana_juego.habilitar_botones)
        self.cliente.senal_botones_jugar_no.connect(self.ventana_juego.inhabilitar_botones)
        self.cliente.senal_cambiar_actual.connect(self.ventana_juego.cambiar_actual)
        self.cliente.senal_reroll.connect(self.ventana_juego.cambiar_dados)
        self.cliente.senal_num_respuesta.connect(self.ventana_juego.handle_num_respuesta)
        self.cliente.senal_info_banner.connect(self.ventana_juego.update_banner)
        self.cliente.senal_mostrar_dados.connect(self.ventana_juego.mostrar_dados)
        self.cliente.senal_popup_muerte.connect(self.ventana_juego.mostrar_popup_muerte)
        self.cliente.senal_ganar.connect(self.ventana_juego.abrir_popup_ganar)
        self.cliente.senal_dead_server.connect(self.ventana_juego.popup_dead_server)
        self.cliente.senal_no_dados.connect(self.ventana_juego.popup_no_poder)
        self.cliente.senal_mostrar_combo.connect(self.ventana_juego.mostrar_combo)
        self.cliente.senal_no_dudar.connect(self.ventana_juego.mostrar_no_duda)

        self.ventana_juego.senal_orden_reroll.connect(self.cliente.enviar_info)
        self.ventana_juego.senal_enviar_num.connect(self.cliente.enviar_info)
        self.ventana_juego.senal_paso.connect(self.cliente.enviar_info)
        self.ventana_juego.senal_dudar.connect(self.cliente.enviar_info)
        self.ventana_juego.senal_boton_poder.connect(self.cliente.enviar_info)
        self.ventana_juego.senal_poder_target.connect(self.cliente.enviar_info)
        self.ventana_juego.senal_cerrar_socket.connect(self.cliente.cerrar_socket)

    def metodos_iniciales(self):
        self.cliente.enviar_diccionario_front()

    def inicializar(self):
        self.ventana_inicio.show()

    def abrir_ventana_juego(self, dict=None, dict2=None):
        self.ventana_juego.show()
        self.ventana_inicio.hide()


if __name__ == '__main__':
    app = QApplication([])
    port = int(sys.argv[1])
    instanciador = Manager(port)
    sys.exit(app.exec_())
