from copy import copy
from functools import reduce
from itertools import groupby
from typing import Generator

from utilidades import (
    Categoria, Producto, duplicador_generadores, generador_a_lista
)


# ----------------------------------------------------------------------------
# Parte 1: Cargar dataset
# ----------------------------------------------------------------------------

def cargar_productos(ruta: str) -> Generator:
    with open(ruta, 'r') as file:
        info = [line.strip().split(',') for line in file.readlines()[1:]]
    for line in info:
        for index in range(len(line)):
            if line[index].isnumeric():
                line[index] = int(line[index])
    for line in info:
        yield Producto(*line)


def cargar_categorias(ruta: str) -> Generator:
    with open(ruta, 'r') as file:
        info = [line.strip().split(',') for line in file.readlines()[1:]]
    for line in info:
        line[1] = int(line[1])
        yield Categoria(*line)
    


# ----------------------------------------------------------------------------
# Parte 2: Consultas sobre generadores
# ----------------------------------------------------------------------------

def obtener_productos(generador_productos: Generator) -> map:
    return map(lambda x: x.nombre, generador_productos)


def obtener_precio_promedio(generador_productos: Generator) -> int:
    duplicado = duplicador_generadores(generador_productos)
    q = len(generador_a_lista(duplicado[1]))
    suma = reduce(lambda x, y: x.precio+y.precio, duplicado[0])
    return int(suma / q)


def filtrar_por_medida(generador_productos: Generator,
                       medida_min: float, medida_max: float, unidad: str
                       ) -> filter:
    filtro = filter(lambda x: x.unidad_medida == unidad and medida_min <= x.medida <= medida_max, generador_productos)
    return filtro


def filtrar_por_categoria(generador_productos: Generator,
                          generador_categorias: Generator,
                          nombre_categoria: str) -> Generator:
    categorias = filter(lambda x: x.nombre_categoria == nombre_categoria, generador_categorias)
    ids = list(map(lambda x: x.id_producto, categorias))
    productos = filter(lambda x: x.id_producto in ids, generador_productos)
    return productos


def agrupar_por_pasillo(generador_productos: Generator) -> Generator:
    groups = groupby(generador_productos, lambda x: x.pasillo)
    return groups


# ----------------------------------------------------------------------------
# Parte 3: Iterables
# ----------------------------------------------------------------------------

class Carrito:
    def __init__(self, productos: list) -> None:
        self.productos = productos

    def __iter__(self):
        return IteradorCarrito(self.productos)


class IteradorCarrito:
    def __init__(self, iterable_productos: list) -> None:
        self.productos_iterable = copy(iterable_productos)

    def __iter__(self):
        return self

    def __next__(self):
        if self.productos_iterable == []:
            raise StopIteration
        else:
            self.productos_iterable.sort(key=lambda x: x.precio)
            return self.productos_iterable.pop(0)
