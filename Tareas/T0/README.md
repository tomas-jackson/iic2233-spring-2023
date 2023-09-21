# Tarea 0: DCCeldas 💣🐢🏰

Bienvenidos a mi Tarea 0 :stuck_out_tongue_winking_eye:, mejor conocida como la historia de como perdi la cabeza intentando idear un algoritmo recursivo para resolver los infernales tableros de DCCeldas :heart_eyes:

PORQUE DIANTRES NO ENSENAN BACKTRACKING EN INTRO, NI SIQUIERA ***:star: UNA SOLA MENCION :star:***, 

Dejando eso atras (jaja, se entiende?), sigo con la explicacion :yum:

[Este video](https://youtu.be/dQw4w9WgXcQ) contextualiza mi estado al terminar esta tarea.

## Consideraciones generales :octocat:
El codigo fue escrito principalmente en español pero existen varias variables definidas en ingles.
Los archivos contenidos en la carpeta **T0** llevan a cabo el flujo principal pedido. 
Los menu funcionan correctamente y no hay errores al entregar inputs invalidos. Se cambio el orden entre la opcion 3 y 4 ya que hacia mas sentido validar la solucion despues de generarla, aun asi, una opcion no depende de otra y si es posible validar un tablero que no ha sido solucionado
La funcion *solucionar_tablero* entrega las soluciones pedidas.
Las funciones corren y retornan los valores pedidos, aun asi, existen muchas oportunidades para hacer codigo mas eficiente, especialmente la funcion *solucionar_tablero*. 
Sin embargo, al no existir limites en el tiempo de ejecucion, se disminuyo la prioridad de realizar estos cambios
### Cosas importantes :innocent:
1. **El menu de inicio recibe nombres de archivo que deben incluir la extension**
2. **Al menu de acciones se le debe entregar el numero de la opcion sin los brackets** 
3. **La funcion** ***solucionar_tablero*** **aumenta muy rapidamente su tiempo de ejecucion para tableros sobre 5x5 pero si entrega tableros validos, en 7x7 el tiempo ya es muy elevado y despues de 1 hora el codigo seguia corriendio pero teoricamente, dado suficiente tiempo, si llegaria una solucion** ```(optimizacion WIP)``` 
4. **Es necesario que exista una carpeta *Archivos* en el directorio del cual se esta ejecutando el codigo** 

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Menú de Inicio (5 pts) (7%)
##### ✅ Seleccionar Archivo
##### ✅ Validar Archivos
#### Menú de Acciones (11 pts) (15%) 
##### ✅ Opciones
##### ✅ Mostrar tablero 
##### ✅ Validar bombas y tortugas
##### ✅ Revisar solución
##### ✅ Solucionar tablero
##### ✅ Salir
#### Funciones (34 pts) (45%)
##### ✅ Cargar tablero
##### ✅ Guardar tablero
##### ✅ Valor bombas
##### ✅ Alcance bomba
##### ✅ Verificar tortugas
##### ✅ Solucionar tablero
#### General: (19 pts) (25%)
##### ✅ Manejo de Archivos
##### ✅ Menús
##### ✅ tablero.py
##### ✅ Módulos
##### ✅ PEP-8
#### Bonus: 6 décimas
##### ✅ Funciones atómicas
##### ❌ Regla 5
## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. 
No es necesario crear archivos adicionales para correr el codigo, todo lo esencial se encuentra en la carpeta T0 subida al repositorio y se espera que se ejecute el codigo desde ahi.
Si se desea, se pueden agregar archivos a la carpeta *Archivos* para que sean probados por el codigo



## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```os.path```: ```exists()```, ```join()```
2. ```collections```: ```deque()``` 


### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```functions.py```: Contiene las funciones necesarias para llevar a cabo el flujo principal del programa
2. ```tablero.py```: Hecha para mostrar en terminal el tablero de una manera mas facil de visualizar

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. *Los archivos entregados van a contener solo 1 punto en su nombre, el separador entre el nombre y su extension. Si bien es un caso que puede pasar, son casos menos comunes que pueden ser solucionados por el usuario mediante un cambio de nombre*
2. *El codigo principal que se encuetra en main.py va a ser corrido desde la carpeta T0 que se encuentra en Tareas/T0 en mi repositorio personal. Asumi esto por que es la manera mas simple y eficiente de probar el codigo, evita tener que copiar o mover cosas a otros directorios*

-------

## Referencias de código externo :book:

Para realizar me inspire en codigo que se encuentra en:
1. [Codigo](https://youtu.be/G_UYXzGuqvM): este soluciona un tablero de sudoku haciendo uso de backtracking y está implementado en el archivo ```functions.py``` en las líneas 280 a 296. Si bien no fue copiado directamente, si lo use como base para armar la funcion que resolveria los distintos tableros entregados



## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/main/Tareas/Descuentos.md).
