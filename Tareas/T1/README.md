# Tarea 1: DCCavaCava 🏖⛏

Bienvenides a la famosa y tan nombrada TAREA 1 (**celebracion**) (**llora**), aca podran encontrar los excavadores mas incompetentes de la historia
y las arenas mas desastrosas del planeta (seriamente, como ocurren tantos desastres naturales?)

Cada dia me doy mas cuenta que programacion avanzada es como estar en una relacion toxica.  

Por ultimo, [un regalo](https://www.youtube.com/watch?v=TFwXbp9bLlY) para ustedes n.n (audio on)

Prosigo con la info importante, pido perdon de antemano por los centenares de linea de codigo que tengo escritas pero hice lo mejor posible para ir explicando
todo con docstrings y comentarios


## Consideraciones generales :octocat:

El codigo fue escrito principalmente en **español** pero existen varias variables escritas en **ingles**. El archivo ```main.py``` que se encuentra en la carpeta **T1** lleva a cabo el flujo pedido, si embargo es necesario la presencia de archivos csv con los datos requeridos para instanciar las clases pedidas; en la seccion de **Ejecucion** se especifican sus requerimientos.

### Cosas importantes
1. **Los menu son robustos ante cualquier input, el programa no se cae al entregar un input invalido**
2. **Para los menus se deben entregar el numero de la opcion sin brackets si la opcion es un digito, o la letra en minuscula sin brackets si la opcion es una letra**
3. **Los menus entregan toda la informacion pedida, no se hicieron modificaciones muy grandes, en el menu de items, al llegar a mas de 10 items en total, los items del 10 en adelante se encuentran desplazados un espacio a la derecha, rompiendo un poco la alineacion del menu**
4. **El guardado y cargado del archivo DCCavaCava.txt se hace correctamente**
5. **Los requerimientos minimos de cada clase son cumplidos, ademas de estos se agregaron varios atributos para facilitar la creacion del flujo principal**
6. **Se utilizo herencia, propiedades y clases abstractas donde se estimo mas conveniente**
7. **Es necesario agregar archivos a la carpeta T1 para que funcione correctamente el codigo**

### Cosas implementadas y no implementadas :white_check_mark: :x: ```si corresponde, el texto en este formato al lado de los titulos muestra donde fue definida esa seccion```


#### Programación Orientada a Objetos: 42 pts (35%)
##### ✅  Diagrama
##### ✅ Definición de clases, atributos, métodos y properties
1.  Realizada en los archivos que comienzan con ```clase_```, mucha relacion entre clases pero la mayoria de los metodos estan documentados para entenderlos mejor no los explico aca porque los importantes tienen un docstring bajo su definicion 
##### ✅ Relaciones entre clases
1. Las relaciones de agregacion, composicion y herencia son aplicadas. Entre Excavador y Torneo tal como entre Arena y Torneo hay relacion de composicion. Items se agregan tanto en Arena, como Torneo. Las herencias son claras en el codigo
#### Preparación programa: 11 pts (9%)
##### ✅ Creación de partidas
1. Las partidas se crean sin problemas, siendo posible iniciar una cantidad indefinida de nuevas partidas. Revisar ```carga_partidas.py``` para ver como se carga una partida existente. La carga de estos datos ocurre sin problema volviendo al estado esperado. Una nueva partida equivale a una instancia de Torneo nueva.
#### Entidades: 22 pts (18%)
##### ✅ Excavador ```clases_excavador.py```
1. Clase abstracta bien definida con sus metodos y propiedades (abstractas segun corresponda). Las caracteristicas minimas pedidas estan bien modeladas, se agregan atributos para facilitar algunos metodos y en ocasiones hacer mas claro el codigo. Las clases heradadas modelan los requerimientos pedidos
##### ✅ Arena ```clases_arena.py```
1. Clase tradicional, cumple con los atributos minimos, le agrego unos atributos extras para hacer mas facil modelar algunas situaciones. La herencia se hace bien cumliendo los requisitos del enunciado
##### ✅ Torneo ```clase_torneo.py```
1. Clase principal, funciones mas importantes, todo lo pedido funciona bien, no existe ningun bug por todo lo que pude probar, se implemento lo minimo y se agregaron algunos atributos para hacer mas facil el codgio en ciertas partes.
#### Flujo del programa: 31 pts (26%)
##### ✅ Menú de Inicio ```main.py```
1. Muestra las opciones pedidas, puede cargar y partir una nueva sin problema. Resiste todo input
##### ✅ Menú Principal ```main.py```
1. Muestra las opciones pedidas, puede volver y salir en todo momento. Todas las opciones funcionan, resitente a todo input
##### ✅ Simulación día Torneo ```clase_torneo.py```
1. En terminal se muestran las 3 fases de la simulacion pedida en el enunciad
##### ✅ Mostrar estado torneo ```clase_torneo.py```
1. En terminal se muestra una tabla con la informacion minima requerida en el enunciado
##### ✅ Menú Ítems ```clase_torneo.py```
1. Los items se muestran correctamente en el menu (que me quedo muy bonito gracias :3), el menu se actualiza cada vez que se usa un item y reordena las posiciones, se adapta a los nombres y descripciones mas largos. Puede volver y salir en todo momento
##### ✅ Guardar partida ```funciones.py```
1. La partida se guarda correctamente en **T1/** en el formato estipulado por yo mismo, con nombre ```DCCavaCava.txt```. La funcion para guardar partida se encuentra en ```funciones.py```
##### ✅ Robustez
1. Si bien no se se usaron excepciones, el codigo es robusto a todo tipo de inputs. 
#### Manejo de archivos: 14 pts (12%)
##### ✅ Archivos CSV ```manejo_archivos.py```
1. Los archivos csv se manejan y leen bien, sin errores de formato.
##### ✅ Archivos TXT
1. El archivo se crea en la carpeta T1, incluye la informacion de un estado de torneo
##### ✅ parametros.py
1. Todas las constantes a utilizar se definen aca, no existen variables globales en otros archivos.
#### Bonus: 3 décimas máximo
##### ✅ Guardar Partida ```funciones.py``
1. completado, solo acepta nombres con letras, ningun caracter especial, el nombre se entrega sin extension, se muestra una lista con todas las partidas disponibles

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```, desde la carpeta T1. Es necesario agregar **4 archivos**. 
Estos son:
1. Archivo con la informacion de excavadores, este debe incluir la informacion necesaria para instanciar cada excavador, una linea por instancia, informacion separada por comas en la disposicion expuesta en el enunciado. Su **path** debe ser exactamente igual al que es estipulado en ```parametros.py``` como *PATH_EXCAVADORES*.
2. Archivo con la informacion de arenas, este debe incluir la informacion necesaria para instanciar cada arena, una linea por instancia, informacion separada por comas en la disposicion expuesta en el enunciado. Su **path** debe ser exactamente igual al que es estipulado en ```parametros.py``` como *PATH_ARENAS*.
3. Archivo con la informacion de tesoros, este debe incluir la informacion necesaria para instanciar cada tesoro, una linea por instancia, informacion separada por comas en la disposicion expuesta en el enunciado. Su **path** debe ser exactamente igual al que es estipulado en ```parametros.py``` como *PATH_TESOROS*.
4. Archivo con la informacion de consumibles, este debe incluir la informacion necesaria para instanciar cada consumible, una linea por instancia, informacion separada por comas en la disposicion expuesta en el enunciado. Su **path** debe ser exactamente igual al que es estipulado en ```parametros.py``` como *PATH_CONSUMIBLES*.

SI ESTOS 4 ARCHIVOS NO SON AGREGADOS CON ESTOS EXACTOS FORMATOS Y DISPOSICION DE LA INFORMACION, **EL PROGRAMA NO PUEDE CORRER**
Una vez se agregan estos 4 archivos el codigo corre sin problema

**IMPORTANTE**: EL ARCHIVO NO SE PUEDE EJECUTAR DE UNA CARPETA QUE NO SEA **T1/** 

**IMPORTANTE**: ES ESENCIAL QUE NO SE CAMBIE O DESAPAREZCA LA CARPETA **Partidas/**


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```random```: ```randint()```, ```choices()```, ```choice()```, ```sample()```
2. ```collections```: ```namedtuple()```
3. ```abc```: ```ABC```, ```abstractmethod()```
4. ```os```: ```path```, ```listdir()```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```clases_torneo```: Contiene todas las clases y codigo necesario para instanciar un objeto de la clase ```Torneo```
2. ```clases_excavador```: Contiene todas las clases y codigo necesario para instanciar un objeto de la clase ```Excavador``` y sus heredadas (```ExcavadorTareo```, ```ExcavadorDocencio```, ```ExcavadorHibrido```)
3. ```clases_arena```: Contiene todas las clases y codigo necesario para instanciar un objeto de la clase ```Arena``` y sus heredadas (```ArenaNormal```, ```ArenaMojada```, ```ArenaRocosa```, ```ArenaMagnetica```)
4. ```clases_items```: Contiene todas las clases y codigo necesario para instanciar un objeto de la clase ```Consumibles``` o ```Tesoros```
5. ```parametros```: contiene las constantes a utilizar para el modelamiento del torneo y sus distintas clases
6. ```funciones```: contiene funciones varias destinadas a facilitar algunas comparaciones, procesos y metodos en el codigo de los distintos archivos, tambien contiene la funcion para guardar partida y la funcion para mostrar el menu de las partidas guardadas(bonus)
7. ```carga_partidas```: contiene el codigo para cargar una partida de DCCavaCava
8. ```manejo_archivos```: lleva acabo la lectura de los archivo de informacion en la carpeta T1/

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Los excavadores no se pueden repetir ya que no tiene sentido tener 2 clones de un mismo excavador
2. Todas las arenas parten con el mismo set de items que incluye a todos los items encontrados en  ```tesoros.csv``` y ```consumibles.csv```, hace sentido si se toma la arena como un mapa que puede ir cambiando, estilo Super Smash Bros
3. Si ocurre una situacion que obliga el cambio de arena, pero la arena actual es del mismo tipo al de la nueva, la arena igualmente cambia. El efecto del tesoro o derrumbe es sobre la arena sin importar su tipo. Un derrumbe si cambiaria el paisaje, del mismo modo que activar un tesoro tambien lo cambiaria.
4. Un excavador descansando se encuentra fuera de juego y no puede excavar, encontrar items o usar consumibles. Si no fuera el caso habria que trabajar con la pregunta de que ocurre si un trabajador descansando ocupa un consumible y gana energia.
5. Las modificaciones a los parametros se van a mantener entre los rangos y tipos estipulados en el enunciado.




-------


## Referencias de código externo :book:

1. Todo el codigo es propio n.n
