# Tarea 3: DCCachos 🎲

CHAN, la ultima tarea por fin. Parece como si hubiera sido hace decadas que partimos el curso y yo andaba alegando sobre que no conocia backtracking, si solo hubiera sabido lo que se venia. Gracias por su labor queride ayudante, le dejo este [video](https://youtu.be/0gw8l7iv2Wg) que es muy bonito y representa mi estado mental despues de terminar esta tarea. La experiencia de revision se vera altamente beneficiada por tenerlo sonando de fondo. Sin mas preambulos, aqui va toda la info de la tarea.

## Consideraciones generales

- En pocas palabras, todo esta implementado menos los bonus.
- Al instanciar los bots se instancia una clase de socket para cada uno, este es simplemente un placeholder,
nunca es conectado al socket del servidor, solamente existen para poder hacer compatibles a los bots con el resto de mi codigo sin requerir una reformulacion de este.
- Para el correcto funcionamiento, clientes en la cola para entrar a sala de espera no pueden cerrar su ventana.
- En la encriptacion, el intercambio del primer byte con el byte N_PONDERADOR solo se realiza cuando el largo del mensaje es mayor o igual a N_PONDERADOR, en otro caso se salta ese paso
- Existen leves delays al apretar botones y despues mostrar el cambio, esto es parte del diseño
- **IMPORTANTE** Todo el desarrollo de la tarea se realizo en MacOS y tengo entendido que esto puede generar problemas de compatibilidad entre tamaños de los labels, llevando a palabras que se vean cortadas o botones que se ven de distinto tamaño en otros OS.
- El puerto del server debe ser igual al puerto del cliente
- En una partida con bots, si el cliente se desconecta cuando esta jugando un bot, el programa deja de correr hasta que otro cliente se desconecte
- Si alguien se desconecta del server, se toma como si murio y por lo tanto se reinicia la ronda y parte la primera persona viva en sentido antihorario


### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Networking: 18 pts (16%)
##### ✅ Protocolo
- Todos los sockets son instanciados en modo IPv4 y TCP, se encuentran en la linea 37 de ```clientes.py``` y 32 de ```server.py```
##### ✅ Correcto uso de sockets
- Los sockets se conectan bien (linea 39 ```clientes.py``` y linea 35 ```server.py```)
- Se instancia un thread para cada cliente que se conecta al servidor por lo que se evita un bloqueo del programa cuando se esta leyendo un socket, similarmente, cada cliente tiene un thread que recibe del server (linea 41 ```clientes.py``` y linea 36 ```server.py```)
##### ✅ Conexión
- La conexion se mantiene durante toda el juego, cualquier desconexion es atrapada con un try/except
##### ✅ Manejo de Clientes
- Se puede conectar una cantidad ilimitada de clientes, siempre y cuando se respete lo escrito en consideraciones generales sobre clientes en cola
##### ✅ Desconexión Repentina
- Una desconexion del server levanta el popup en ventanas
- Un cliente se puede desconectar en cualquier momento sin afectar el funcionamiento de la partida
#### Arquitectura Cliente - Servidor: 18 pts (16%)
##### ✅ Roles
- Toda la verificacion de valores y movimientos es realizada en el servidor, el frontend del cliente solo se encarga de activar o desactivar botones y de enviar popups
- El cliente solo se encarga de enviar las acciones de jugador al server y de mostrar las respuestas del server en la ventana
- La carpeta ```cliente``` es independiente de la carpeta ```servidor```
##### ✅ Consistencia
- Se utiliza un lock cuando se envia mensajes, no fue necesario en otro momento para mantener la info igual entre clientes
- La info general que todos deben saber se mantiene actualizada en todos los clientes, los dados muestran la seleccion actual
##### ✅ Logs
- Los logs representan todos los eventos pedidos
#### Manejo de Bytes: 26 pts (22%)
##### ✅ Codificación
- Si, linea 62 - 74, 81, 85 de  ```cripto.py```
##### ✅ Decodificación
- Si, linea 91 - 102 de ```cripto.py```
##### ✅ Encriptación
- Sip, como fue mencionado, no se hizo el cambio del N_PONDERADOR por el primer byte cuando el largo del array era menos a los bytes porque este N_PONDERADOR efectivamente existia como un minimo de bytes que podia ser un mensaje
##### ✅ Desencriptación
- Sip
##### ✅ Integración
- Sip, en las funciones para enviar info tanto de ```clientes.py``` como de ```server.py```
#### Interfaz Gráfica: 22 pts (19%)
##### ✅ Ventana de Inicio
- Se mantiene al dia con la informacion, tiene todos los popups pedidos, tanto si hay una sala llena o si la partida ya inicio, todos los botones funcionan
##### ✅ Ventana de juego
- Se mantiene al dia con la informacion, los dados solo se muestran al jugador correspondiente a menos que seleccione dudar, todos los botones funcionan y cumplen lo pedio en el enunciado, todos los popups funcionan
#### Reglas de DCCachos: 22 pts (19%)
##### ✅ Inicio del juego
- Se define al azar el primero y se mueve en direccion antihoraria, la seleccion de dados se realiza en la linea 235 de ```server.py```
##### ✅ Bots
- Los bots son definidos en el archivo ```utility.py```, ahi se puede ver su secuencia de juego
##### ✅ Ronda
- Se checkea restriccion (linea 272 - 285 ```server.py```)
- Todas las restricciones de las acciones son implementadas, tanto la de relanzar dados, como la de pasar y la de anunciar valor
- Se checkea el valor de los dados (linea 123 a 129 ```utility.py``` y linea 367 a 382 ```server.py```)
##### ✅ Termino del juego
- El juego termina bien y se anuncia un ganador, incluso si son solo bots
#### Archivos: 10 pts (9%)
##### ✅ Parámetros (JSON)
- Archivos en carpeta ```cliente``` y carpeta ```server```, contienen toda la informacion necesaria
- Los archivos se cargan en ```cripto.py```, ```server.py``` y ```ventana_juego.py```
##### ✅ main.py
- El puerto debe ser entregado
##### ✅ Cripto.py
- ```cripto.py``` esta bien implementado y utilizado en ```clientes.py``` y ```server.py```
#### Bonus: 4 décimas máximo
##### ❌ Cheatcodes
##### ❌ Turno con tiempo

## Ejecución :computer:

El working directory al ejecutar el codigo debe ser la carpeta ```T3```. Dentro de esta, el archivo principal para ejecutar el server tiene el directorio ```servidor/main.py``` y mientras que el del cliente es ```cliente/main.py```. Al no subirse al repo, es necesario agregar la carpeta ```Sprites``` con los mismos contenidos y directorios que la que fue subida con el enunciado de la tarea. A parte de eso no es necesario agregar ningun archivo.

## Librerías :books:

### Librerías externas utilizadas

La lista de librerías externas que utilicé es la siguiente:

1. ```os```: ```join()```
2. ```PyQt5```: ```QtWidgets```, ```QtGui```, ```QtCore```, ```uic```  (debe instalarse)
3. ```threading```: ```Thread```, ```Lock```
4. ```random```: ```choices()```, ```choice()```, ```randint```
5. ```sys```: ```exit()```, ```argv```
6. ```socket```: ```socket```, ```sendall()```, ```bind()```, ```listen()```, ```connect()```, ```close()```, ```accept()```
7. ```collections```: ```namedtuple()```, ```deque()```
8. ```time```: ```sleep()```
9. ```json```: ```load()```, ```loads()```, ```dumps()```, ```encode()```, ```decode()```

### Librerías propias

Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```utility```: contiene clase ```Bot``` y funciones varias para facilitar distintas funcionalidades
2. ```cripto```: Contiene las funciones que encriptan y decriptan los mensajes del servidor

## Supuestos y consideraciones adicionales :thinking:

Los supuestos que realicé durante la tarea son los siguientes:

1. Solo se considera conectada una persona que encontro un espacio libre en la sala de espera, en cualquier otra caso, se considera en espera y los nombres solo muestran 'Buscando...', por esto no se le asigna nombre a una persona esperando a entrar a la sala
2. Un cliente que recibe el popup de muerte o victoria se considera desconectado por lo que, si el servidor se desconecta, no se abre el popup de desconexion del server.


-------


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. AYUDANTIA 10: este es el codigo base tanto del cliente como del servidor, es decir, la implementacion de threads para recibir la info del socket conectado, la implementacion del sistema para leer los bytes recibidos del servidor. Se encuentra en ```clientes.py``` y ```servidor.py```



