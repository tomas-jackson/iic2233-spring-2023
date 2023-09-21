from PyQt5.QtWidgets import QApplication
from frontend_constructor import VentanaConstructor
from frontend_inicio import VentanaInicio
from backend_inicio import ProcesadorInicio
from backend_constructor import ProcesadorConstructor
from frontend_juego import VentanaJuego
from backend_juego import ProcesadorJuego
import sys


class InstanciadorJuego():
    def __init__(self):
        self.v_inicio = VentanaInicio()
        self.p_inicio = ProcesadorInicio()
        self.v_constru = VentanaConstructor()
        self.p_constru = ProcesadorConstructor()
        self.v_juego = VentanaJuego()
        self.p_juego = ProcesadorJuego()
        self.conectar_señales()
        self.metodos_iniciales()
        self.v_inicio.show()

    def conectar_señales(self):
        # señales frontend backend de la ventana de inicoio
        self.p_inicio.senal_info_mapa.connect(self.v_inicio.actualizar_combo_box)
        self.v_inicio.senal_inicio.connect(self.p_inicio.verificar_informacion)
        self.p_inicio.senal_start.connect(self.v_inicio.iniciar_partida)
        self.v_inicio.senal_iniciar_constructor.connect(self.iniciar_constructor)
        self.v_inicio.senal_enviar_user.connect(self.p_constru.setear_user)

        self.v_inicio.senal_enviar_user.connect(self.p_juego.setear_user)
        self.v_inicio.senal_enviar_map_name.connect(self.p_juego.leer_grilla)
        self.v_inicio.senal_iniciar_juego.connect(self.iniciar_juego)
        self.v_inicio.senal_iniciar_juego.connect(self.p_juego.iniciar_timer_juego)
        self.v_inicio.senal_iniciar_juego.connect(self.p_juego.iniciar_timer_fantasma)

        # señales front and back del constructor
        self.p_constru.senal_grilla.connect(self.v_constru.receive_set_grilla)
        self.p_constru.senal_cant_disponible.connect(self.v_constru.actualizar_cant_botones)
        self.p_constru.senal_ventana_error_pos.connect(self.v_constru.abrir_ventana_error)
        self.v_constru.senal_actualizar_cantidad.connect(self.p_constru.enviar_instancias_disponibles)
        self.v_constru.senal_boton_seteado.connect(self.p_constru.procesar_enviar_boton_seteado)
        self.v_constru.senal_limpiar_grilla.connect(self.p_constru.limpiar_grilla)
        self.v_constru.senal_iniciar_juego.connect(self.p_constru.enviar_grilla_inicio_juego)
        self.v_constru.senal_iniciar_juego.connect(self.p_juego.iniciar_timer_juego)
        self.v_constru.senal_iniciar_juego.connect(self.p_juego.iniciar_timer_fantasma)

        # señales front and back del juego
        self.p_constru.senal_enviar_grilla_juego.connect(self.p_juego.recibir_setear_grilla_inicio)
        self.p_juego.senal_grilla.connect(self.v_juego.receive_set_grilla)
        self.p_juego.senal_constructor_juego.connect(self.iniciar_juego)
        self.v_juego.senal_validar_luigi.connect(self.p_juego.validar_nueva_pos_luigi)
        self.p_juego.senal_can_luigi_move.connect(self.v_juego.cambiar_estado_movimiento_luigi)
        self.p_juego.senal_actualizar_vidas.connect(self.v_juego.actualizar_label_vidas)
        self.p_juego.senal_rock_move.connect(self.v_juego.mover_roca)
        self.p_juego.senal_reset_grilla.connect(self.v_juego.resetear)
        self.p_juego.senal_sobre_estrella.connect(self.v_juego.cambiar_sobre_estrella)
        self.p_juego.senal_juego_countdown.connect(self.v_juego.actualizar_countdown)
        self.v_juego.senal_cambiar_pausa.connect(self.p_juego.cambiar_estado_pausa)
        self.p_juego.senal_muerte.connect(self.v_juego.abrir_ventana_muerte)
        self.v_juego.senal_new_game.connect(self.p_juego.resetear_grilla_new_game)
        self.p_juego.senal_timeout.connect(self.v_juego.abrir_ventana_timeout)
        self.p_juego.senal_sacar_fantasma_mapa.connect(self.v_juego.sacar_fantasma)
        self.p_juego.senal_movimiento_valido_fant.connect(self.v_juego.mover_fantasma)
        self.p_juego.senal_puntaje_final.connect(self.v_juego.actualizar_puntaje)
        self.v_juego.senal_orden_puntaje.connect(self.p_juego.enviar_puntaje)
        self.v_juego.senal_genocidio.connect(self.p_juego.genocidio)
        self.p_juego.senal_label_infinito.connect(self.v_juego.actualizar_label_vidas)
        self.v_juego.senal_vidas_infinitas.connect(self.p_juego.setear_vidas_infinitas)

    def metodos_iniciales(self):
        self.p_inicio.extraer_mapas()
        self.p_constru.enviar_grilla()
        self.p_constru.enviar_instancias_disponibles()

    def iniciar_constructor(self):
        self.v_inicio.hide()
        self.v_constru.show()

    def iniciar_juego(self):
        self.v_inicio.hide()
        self.v_constru.hide()
        self.v_juego.show()


if __name__ == '__main__':
    app = QApplication([])
    instanciador = InstanciadorJuego()
    sys.exit(app.exec_())
