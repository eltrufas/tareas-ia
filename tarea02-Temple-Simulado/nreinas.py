#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nreinas.py
------------

Ejemplo de las n_reinas con búsquedas locales

"""

__author__ = 'juliowaissman'


from blocales import descenso_colinas, temple_simulado, reinicios_aleatorios, \
    Problema
from random import shuffle
from random import sample
from itertools import combinations, takewhile
from operator import itemgetter
import time


class ProblemaNReinas(Problema):
    """
    Las N reinas en forma de búsqueda local se inicializa como

    entorno = ProblemaNreinas(n) donde n es el número de reinas a colocar

    Por default son las clásicas 8 reinas.

    """
    def __init__(self, n=8):
        self.n = n

    def estado_aleatorio(self):
        estado = list(range(self.n))
        shuffle(estado)
        return tuple(estado)

    def vecinos(self, estado):
        """
        Generador vecinos de un estado, todas las 2 permutaciones

        @param estado: una tupla que describe un estado.

        @return: un generador de estados vecinos.

        """
        edo_lista = list(estado)
        for i, j in combinations(range(self.n), 2):
            edo_lista[i], edo_lista[j] = edo_lista[j], edo_lista[i]
            yield tuple(edo_lista)
            edo_lista[i], edo_lista[j] = edo_lista[j], edo_lista[i]

    def vecino_aleatorio(self, estado):
        """
        Genera un vecino de un estado intercambiando dos posiciones
        en forma aleatoria.

        @param estado: Una tupla que describe un estado

        @return: Una tupla con un estado vecino.

        """
        vecino = list(estado)
        i, j = sample(range(self.n), 2)
        vecino[i], vecino[j] = vecino[j], vecino[i]
        return tuple(vecino)

    def costo(self, estado):
        """
        Calcula el costo de un estado por el número de conflictos entre reinas

        @param estado: Una tupla que describe un estado

        @return: Un valor numérico, mientras más pequeño, mejor es el estado.

        """

        rows = [0] * self.n
        cols = [0] * self.n
        fdiags = [0] * (self.n * 2 - 1)
        bdiags = [0] * (self.n * 2 - 1)

        for x, y in enumerate(estado):
            rows[y] += 1
            cols[x] += 1

            fdiag = self.n - 1 + y - x
            bdiag = x + y

            fdiags[fdiag] += 1
            bdiags[bdiag] += 1

        return (sum(i for i in rows if i > 1) +
                sum(i for i in cols if i > 1) +
                sum(i for i in fdiags if i > 1) +
                sum(i for i in bdiags if i > 1))


def prueba_algoritmo(problema, algoritmo, repeticiones=1):
    """
    Prueba un algoritmo
    """
    for _ in range(repeticiones):
        start = time.time()
        solucion = algoritmo(problema)
        end = time.time()
        elapsed = end - start
        yield solucion, problema.costo(solucion), elapsed


def correr_pruebas(Problema, algoritmo, tiempo_razonable=3600,
                   rango_pruebas=(4, 1000), repeticiones=5):
    pruebas = (prueba_algoritmo(Problema(n),
                                algoritmo,
                                repeticiones)
               for n in range(*rango_pruebas))

    for n, corridas in zip(range(*rango_pruebas), pruebas):
        corridas = list(corridas)
        tiempo_promedio = sum(c[2] for c in corridas) / len(corridas)
        yield n, tiempo_promedio
        if tiempo_promedio > tiempo_razonable:
            break


if __name__ == "__main__":

    # prueba_descenso_colinas(ProblemaNreinas(32), 10)
    # prueba_temple_simulado(ProblemaNreinas(32))

    ##########################################################################
    #                          20 PUNTOS
    ##########################################################################
    #
    # ¿Cual es el máximo número de reinas que se puede resolver en
    # tiempo aceptable con el método de 10 reinicios aleatorios?
    #
    # ¿Que valores para ajustar el temple simulado son los que mejor
    # resultado dan? ¿Cual es el mejor ajuste para el temple simulado
    # y hasta cuantas reinas puede resolver en un tiempo aceptable?
    #
    # En general para obtener mejores resultados del temple simulado,
    # es necesario utilizarprobar diferentes metdos de
    # calendarización, prueba al menos otros dis métodos sencillos de
    # calendarización y ajusta los parámetros para que funcionen de la
    # mejor manera
    #
    # Escribe aqui tus conclusiones
    #
    # ------ IMPLEMENTA AQUI TU CÓDIGO ---------------------------------------
    #

    """
    La función de costo original usaba las combinaciones, lo que le daba una
    complejidad factorial. Al reemplazarla por una funcion lineal mas
    razonable, vemos una mejora de 5x para la solucion de 32 reinas (18
    segundos contra 3 segundos en mi laptop para hacer 10 corridas del decenso
    de colinas y una del temple simulado). Esto nos da el poder de realizar
    corridas mucho mas rapidas. Habiendo logrado esto, vamos a reducir nuestra
    noción de tiempo aceptable de una hora a dos minutos.

    Probando, podemos ver que el decenso de colinas logra encontrar soluciones
    para alrededor de 110 reinas en alrededor de 2 minutos. Los resultados estan
    en el archivo 'decesnso_colinas.txt'. El numero es relativamente bajo
    porque el numero de vecinos que tiene un estado crece rapidamente en el
    problema de las N reinas.

    Por otro lado, la cantidad de reinas no es tan importante para el temple
    simulado. Para el calendarizador incluido, el temple simulado exitosamente
    encuentra soluciones para problemas de mas de 600 reinas.

    Probando un enfriamiento lineal y uno exponencial, encontramos resultados
    similares.
    """



    """ ESTAS PRUEBAS TOMAN MUCHO TIEMPO """
    descenso_con_repeticiones = reinicios_aleatorios(descenso_colinas,
                                                     repeticiones=10)


    # prueba del decenso de colinas con 10 reinicios aleatorios
    pruebas = correr_pruebas(ProblemaNReinas,
                             descenso_con_repeticiones,
                             tiempo_razonable=120,
                             rango_pruebas=(4, 1000))



    with open('descenso_colinas.txt', 'w') as fp:
        print('Pruebas con descenso de colinas con 10 reinicios aleatorios')
        fp.write('Pruebas con descenso de colinas con 10 reinicios aleatorios\n')
        for n, tiempo in pruebas:
            fp.write('{} {}\n'.format(n, tiempo))
            print(n, tiempo)

    # prueba del temple simulado
    pruebas = correr_pruebas(ProblemaNReinas,
                             temple_simulado,
                             tiempo_razonable=120,
                             rango_pruebas=(4, 1000))

    with open('temple_simulado.txt', 'w') as fp:
        print('Pruebas con temple simulado con calendarización To/(1 + i)."')
        fp.write('Pruebas con temple simulado con calendarización To/(1 + i)."\n')
        for n, tiempo in pruebas:
            fp.write('{} {}\n'.format(n, tiempo))
            print(n, tiempo)
