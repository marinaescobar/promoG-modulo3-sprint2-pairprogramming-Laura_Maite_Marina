from src import funciones as fun

productos, clientes, ventas = fun.archivos()

fun.exploracion(productos, clientes, ventas)

clientes_limpio = fun.limpieza(clientes,productos,ventas)
clientes_limpio

nulos = clientes.isnull().sum()
nulos

tabla=fun.union(productos, clientes, ventas)
tabla.head()

final= fun.transformacion(tabla)
final.head()


