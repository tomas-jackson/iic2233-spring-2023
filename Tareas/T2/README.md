# Tarea 2: DCCazafantasmas 👻🧱🔥

Bienvenides al penultimo readme del ramo yujuuu. Pondria un video como en los dos anteriores pero son las 3 de la mañana y estoy exhaustp. Maldito seas Luigi
Comentario que queria hacer, es incomparable la longitud de esta tarea con las dos anteriores, eso, igual me entretuve haciendola, un buen desafio. 
Dicho esto, seguimos con la explicacion de la tarea.

## Consideraciones generales :octocat:

- Durante el desarrollo de la tarea hice mi mejor intento para hacer un uso no excesivo de memoria, sin embargo, despues de un tiempo extendido en un mapa, reiniciando y volviendo a jugar, el juego puede empezar a caer en FPS
- No implemente superposicion de fantasmas
- Los sprites deben tener el mismo nombre que los entregados, a menos que se cambie el nombre en el archivo de parametros.
- En el modo constructor, luego de elegir un boton y soltar el icono en el mapa, el boton 'fuente' todavia se ve presionado, esto es algo meramente estetico y todavia tiene habilitado el drag and drop, si es que quedan elementos
- Al entrar del modo constructor al modo juego principal, aparece un bloque en la ezquina superior de la derecha, este es meramente estetico y no afecta el funcionamiento de la tarea
- Los paths de los sprites son referenciados directamente en el frontend de las ventanas, era muy anti intuitivo cargar sprites en el backend y moverlas al frontend, repitiendo cada una para cada sprite
- Todo el resto considerado, todos los aspectos de la tarea si son implementados, menos los que no estan marcados en verde en la lista de abajo.

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Ventanas: 27 pts (27%)
##### ✅ Ventana de Inicio
- se verifica user, si no es valido se muestra la razon, se verifica seleccion de mapa y se carga satisfactoriamente
##### ✅ Ventana de Juego
- todas las funcionalidades pedidas son implementadas, tanto en la ventana de juego principal como la ventana del modo constructor
#### Mecánicas de juego: 47 pts (47%)
##### ✅ Luigi
- luigi se puede mover por todos lados que esten libres y mueve rocas, al hacerse dano vuelve a su posicion inicial, el juego termina si se hace dano sin vidas
##### 🟠 Fantasmas
- todos los fantasmas son independientes el uno del otro, propia velocidad y estado de muerte o vida, lo que no logre implementar, sin destruir los sprites del mapa, fue hacer que se superponieran
##### ✅ Modo Constructor
- botones representan bien el objeto que se esta seleccionando, al darle inicio al juego se traspasa bien al modo jugar, se puede limpiar, los limites de entidades se respetan, no se inicia a menos que haya un luigi y una estrella
##### ✅ Fin de ronda
- todo bien implementado, se emite sonido, se muestra user, se muestra puntaje, se da la opcion de salir o jugar de nuevo el nivel
#### Interacción con el usuario: 14 pts (14%)
##### ✅ Clicks
- todas las interacciones relevantes son a traves de clicks izquierdos (exceptuando drag and drop y )
##### ❌ Animaciones
- elegi creer y creo que elegi mal
#### Funcionalidades con el teclado: 8 pts (8%)
##### ✅ Pausa
- funciona con todo lo pedido, ni luigi ni fantasmas se pueden mover hasta que se aprete la tecla de nuevo
##### ✅ K + I + L 
- implementado apretando las teclas al mismo tiempo, funciona correctamente
##### ✅ I + N + F
- implementado apretando las teclas al mismo tiempo, funciona correctamente, no cambia el label del countdown, pero si hace que deje de cambiar
##### ✅ Parametros.py
- paths y constantes todas definidas en el archivo
#### Bonus: 8 décimas máximo
##### ✅ Volver a Jugar
- al presionar el boton de las ventanas que aparecen al perder o ganar, el juego se reinicia
##### ❌ Follower Villain
##### ✅ Drag and Drop
- botones arrastrables del borde del modo constructor al mapa principal

## Ubicacion items coloreados distribucion de puntajes
- para señales voy a indicar en que lugar se conecta la señal, de este modo se puede saltar a la definicion de esta, del metodo que la emite (con Ctrl + F) y a la definicion del slot de manera mas rapida
### Ventana Inicio
#### Item 1 - Verificacion de Nombre:
- ```principal.py``` : linea 26
#### Item 2 - Seleccion de mapa:
- ```principal.py``` : linea 26
#### Item 3 - Boton Salir cierra ventana:
- ```frontend_inicio.py```: linea 126

### Ventana Juego
#### Item 1 - Actualizacion datos:
- ```principal.py```: linea 54 y linea 58
#### Item 2 - Juego Inicia con boton:
- ```principal.py```: linea 33 - 35 y 44 - 46
#### Item 3 - Boton salir cierra:
- ```principal.py```: linea 278, 291, 304

### Luigi
#### Item 1 - Daño y resetea:
- ```backend_juego.py```: linea 139 - 141
#### Item 2 - Colisionar y mover roca:
- ```principal.py```: linea 53 y 55
#### Item 3 - Consistencia con movimiento:
- ```frontend_juego.py```: metodo de la linea 142, keyPressEvent()

### Fantasma
#### Item 1 - Fantasmas individuales:
- ```entidades.py```: las clases en las lineas 16 y 55
- ```principal.py```: linea 64
#### Item 2 - velocidad random:
- ```entidades.py```: linea 25 y linea 64

### Modo Constructor
#### Item 1 - Maximo de elementos:
- ```backend_consructor.py```: metodo que se define en linea 61
#### Item 2 - Requerimientos de Inicio:
- ```principal.py```: linea 44 - 49
- ```frontend_constructor```: metodo en linea 249

### Fin de Ronda
#### Item 1 - Calculo puntaje:
- ```backend_juego.py```: metodo definido en linea 245
#### Item 2 - Boton Salir;
- ```frontend_juego.py```: linea 271 - 308

### Funcionalidades Teclado
#### Item 1 - Pausa:
- ```principal.py```: linea 59
#### Item 2 - INF:
- ```frontend_juego.py```: linea 186 a 189
- ```principal.py```: linea 69
#### Item 3 - KIL:
- ```frontend_juego.py```: linea 191 a 194
- ```principal.py```: linea 67

### Archivos
#### Item 1 - Sprites:
- ```frontend_juego.py```: linea 62, metodo receive_set_grilla()
- ```frontend_constructor.py```: linea 107 (instanciar_botones) y linea 168 (receive_set_grilla())
- ```frontend_inicio.py```:  linea 69, iniciar_gui()

#### Item 2 - Parametros:
- Todos los archivos importan parametros


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```principal.py```. Los archivos de codigo esenciales para correr el codigo todos se encuentran contenidos
en esta carpeta. Sin embargo, para el correcto uso del programa es necesario agregar una carpeta de sprites, una de mapas y una de sonidos. Si es que los nombres de archivo 
de estos elementos son distintos a los entregados para realizar la tarea, estos deben ser cambiados en las rutas escritas en ```parametros.py```. Una vez agregadas las carpetas, el
codigo puede correr sin problemas


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```PyQt5```: ```QtWidgets```, ```QtCore```, ```QtGui```, ```QtMultimedia``` (debe instalarse)
2. ```os```: ```path``` , ```listdir()```
3. ```copy```: ```deepcopy()```
4. ```random```: ```uniform()```
5. ```sys```


### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```entitades```: Contiene las clases que modelan a los objetos dentro del juego
2. ```widgets_custom```: Contiene widgets que heredan de widgets de pyqt5
3. ```ventanas_extra```: Contiene ventanas extras que se muestran cuando el jugador gana o pierde
4. ```frontend_juego```: Contiene la ventana del juego principal
5. ```backend_juego```: Contiene la logica del juego principal
4. ```frontend_constructor```: Contiene la ventana del constructor
5. ```backend_constructor```: Contiene la logica del juego constructor
4. ```frontend_inicio```: Contiene la ventana de inicio
5. ```backend_inicio``: Contiene la logica del inicio
## Supuestos y consideraciones adicionales :thinking:
Me guie completamente por los supuestos entregados en el enunciado, no formule ninguno nuevo, todas las consideraciones relevantes fueron descritas en la seccion de mas arriba.

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. [El codigo](https://www.pythonguis.com/faq/pyqt-drag-drop-widgets/): este convierte el QPushButton en un boton arrastable y está implementado en el archivo ```widgets_custom.py```.
