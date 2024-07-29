Nicolas Caceres Plaza
20828633-1

Ocuparemos los modulos de transformations, basic_shapes y easy_shaders en mayor parte
Adicionalmente en main.py se decidio agregar lighting_shaders y performance_monitor de forma opcional

*********
esfera.py
*********
Este módulo se encarga de la creación de las esferas y las colisiones

Para crear las esferas, usamos la parametrización de los vertices usando coordenadas esféricas de la forma:
x = r sin θ cos φ
y = r sin θ sin φ
z = r cos θ
Luego, definimos vertices los cuales conectaremos creando triángulos
En este punto se usará el módulo vector3 el cual nos ayudará a calcular la normal(normalizada) entre 3 puntos.

Definida ya nuestra esfera, crearemos la clase Ball la cual almacenará las variables de la esfera y manejará las colisiones
Tendremos 2 tipos de colisones: con los bordes y con otras esferas
Al colisionar con el borde se invertirá la velocidad del eje correspondiente
Por otro lado, para colisionar esferas, nos fijaremos en si la distancia entre los centros de la esferas es menor o igual a la suma de sus radios

*******
main.py
*******
Definiremos:
>El controlador como visto en tareas/aux pasados
>La funcion on_key para registrar inputs
>La funcion createGPUShape para simplicar la creacion de figuras mas adelante

Iniciamos glfw y una ventana de 1280 * 720 (16:9)
Colocamos el callback de los inputs
Definimos 2 pipelines (para los shaders)
Definimos el color del fondo y activamos el 3d
Creamos la caja usando createColorNormalsCube y creamos nuestras 2 esferas
Creamos la camara y empezamos el ciclo while
Usamos performanceMonitor para ver el rendimiento y ocuparlo mas adelante en el update
Definimos los parametros de la camara y su rotación
Creamos los ejes y las luces (lightingShaders)
Dibujamos nuestro cubo, las esferas y hacemos que se revisen las colisiones constantemente
Finalmente hacemos swap de buffers y limpiamos la memoria

******************
Errores conocidos:
******************
Los parametros de velocidad y posicion no pude dejarlos como lo especificado, al hacer que las esferas partieran de la misma posición daba errores,
que pienso poder haber solucionado cambiando el contador de _ignore_collision en esfera pero no se realizó por tiempo. Debido a esto, cuando se
generan esferas muy juntas suele aparecer solo 1
