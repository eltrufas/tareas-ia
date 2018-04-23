#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
conecta4.py.py
------------

El juego de conecta 4

Este juego contiene una parte de la tarea 5, y otra parte
es la implementación desde 0 del juego de Otello.

"""
from busquedas_adversarios import JuegoSumaCeros2T
from busquedas_adversarios import minimax
from random import shuffle
import tkinter as tk

__author__ = 'juliowaissman'


class ConectaCuatro(JuegoSumaCeros2T):
    def __init__(self):
        """
        Inicializa el juego, esto es: el número de columnas y
        renglones y el estado inicial del juego. Cuyas posiciones
        estan dadas como:

                        35  36  37  38  39  40  41
                        28  29  30  31  32  33  34
                        21  22  23  24  25  26  27
                        14  15  16  17  18  19  20
                         7   8   9  10  11  12  13
                         0   1   2   3   4   5   6
        """
        super().__init__(tuple([0 for _ in range(6 * 7)]))

    def jugadas_legales(self):
        """
        Las jugadas legales son las columnas donde se puede
        poner una ficha (0, ..., 6), si no está llena.
        """
        return (j for j in range(7) if self.x[35 + j] == 0)

    def terminal(self):
        x = self.x
        # Primero checamos filas y diagonales
        if any((xj != 0 for xj in x[21:28])):
            # Filas
            for i in range(7):
                if x[i + 21] == 0 or x[i + 14] != x[i + 21]:
                    continue
                if ((x[i] == x[i + 7] == x[i + 14]) or
                        (x[i + 7] == x[i + 14] == x[i + 28]) or
                        (x[i + 14] == x[i + 28] == x[i + 35])):
                    return x[i + 14]
            # Diagonales
            for j in (0, 7, 14):
                for i in (0, 1, 2, 3):
                    # Hacia arriba
                    if (x[i + j + 24] != 0 and
                            x[i + j + 24] == x[i + j + 16] and
                            x[i + j + 16] == x[i + j + 8] and
                            x[i + j + 8] == x[i + j]):
                        return x[i + j]
                    # Hacia abajo
                    if (x[i + j + 21] != 0 and
                            x[i + j + 21] == x[i + j + 15] and
                            x[i + j + 15] == x[i + j + 9] and
                            x[i + j + 9] == x[i + j + 3]):
                        return x[i + j + 3]
        # Ahora checamos renglones
        for i in range(0, 41, 7):
            if x[i + 3] == 0:
                break
            for j in range(4):
                if (x[i + j] == x[i + j + 1] == x[i + j + 2] == x[i + j + 3]):
                    return x[i + 3]
        # Ahora checamos si no se lleno el tabero
        if 0 not in x:
            return 0
        return None

    def hacer_jugada(self, jugada):
        for i in range(0, 41, 7):
            if self.x[i + jugada] == 0:
                self.x[i + jugada] = self.jugador
                self.historial.append(jugada)
                self.jugador *= -1
                return None

    def deshacer_jugada(self):
        pos = self.historial.pop()
        for i in (35, 28, 21, 14, 7, 0):
            if self.x[i + pos] != 0:
                self.x[i + pos] = 0
                self.jugador *= -1
                return None


def utilidad_c4(juego):
    """
    Calcula la utilidad de una posición del juego conecta 4
    para el jugador max (las fichas rojas, o el que empieza)

    @param x: Una lista con el estado del tablero

    @return: Un número entre -1 y 1 con la ganancia esperada

    Para probar solo busque el número de conecciones de las
    bolitas de mas arriba con su alrededor
    """
    x = juego.x
    cum = 0
    for i in range(7):
        for j in (35, 28, 21, 14, 7, 0):
            if x[i] != 0:
                if 0 < i < 6:
                    biases = (-6, -7, -8, -1, 1, 6, 8)
                elif i == 0:
                    biases = (-7, -8, 1, 8)
                else:
                    biases = (-6, -7, -1, 6)
                con = sum(x[i] for bias in biases
                          if i + bias >= 0 and x[i] == x[i + bias])
                cum += con / len(biases)
                break

    return cum / 42


def ordena_jugadas(juego):
    """
    Ordena las jugadas de acuerdo al jugador actual, en función
    de las más prometedoras.

    Para que funcione le puse simplemente las jugadas aleatorias
    pero es un criterio bastante inaceptable

    """
    def revisar(jugada):
        juego.hacer_jugada(jugada)
        terminal = juego.terminal()
        terminal = terminal if terminal else 0
        juego.deshacer_jugada()
        return juego.jugador * terminal

    jugadas = list(juego.jugadas_legales())
    jugadas.sort(key=revisar)
    return jugadas


class Conecta4GUI:
    def __init__(self, tmax=10, escala=1):

        # La tabla de transposición
        self.tr_ta = {}

        # Máximo tiempo de búsqueda
        self.tmax = tmax

        self.app = app = tk.Tk()
        self.app.title("Conecta Cuatro")
        self.L = L = int(escala) * 50

        tmpstr = "Escoge color, rojas empiezan"
        self.anuncio = tk.Message(app, bg='white', borderwidth=1,
                                  justify=tk.CENTER, text=tmpstr,
                                  width=7*L)
        self.anuncio.pack()

        barra = tk.Frame(app)
        barra.pack()
        botonR = tk.Button(barra, command=lambda x=True: self.jugar(x),
                           text='(re)iniciar con rojas', width=22)
        botonR.grid(column=0, row=0)
        botonN = tk.Button(barra, command=lambda x=False: self.jugar(x),
                           text='(re)iniciar con negras', width=22)
        botonN.grid(column=1, row=0)

        ctn = tk.Frame(app, bg='black')
        ctn.pack()

        self.sel_j = tk.IntVar(self.anuncio.master, -1, 'sel_j')

        def boton_f(fila):
            self.sel_j.set(fila)

        self.flecha = tk.PhotoImage(file='flecha2.gif')
        self.botones = [None for _ in range(7)]
        for i in range(7):
            self.botones[i] = tk.Button(ctn, image=self.flecha,
                                        command=lambda fila=i: boton_f(fila),
                                        width=L, height=L,
                                        state=tk.DISABLED)
            self.botones[i].grid(column=i, row=0)

        self.can = [None for _ in range(6 * 7)]
        self.cuadritos = [None for _ in range(6 * 7)]
        for i in range(6 * 7):
            self.can[i] = tk.Canvas(ctn, height=L, width=L,
                                    bg='light grey', borderwidth=0)
            self.can[i].grid(row=((41 - i) // 7) + 1, column=i % 7)
            self.cuadritos[i] = self.can[i].create_oval(5, 5, L, L,
                                                        fill='white', width=2)
            self.can[i].val = 0

    def jugar(self, primero):

        juego = ConectaCuatro()

        for i in range(42):
            if self.can[i].val != 0:
                self.can[i].itemconfigure(self.cuadritos[i], fill='white')
                self.can[i].val = 0
        color, color_p = 'red', 'black'

        if not primero:
            color, color_p = 'black', 'red'
            self.anuncio['text'] = "Ahora juega Python"
            self.anuncio.update()
            for i in range(7):
                self.botones[i]['state'] = tk.DISABLED

            jugada = minimax(juego, dmax=6, utilidad=utilidad_c4,
                             ordena_jugadas=ordena_jugadas,
                             transp=self.tr_ta)
            juego.hacer_jugada(jugada)
            self.actualiza_tablero(jugada, color_p)

        for _ in range(43):
            self.anuncio['text'] = "Te toca jugar"
            self.anuncio.update()
            for i in juego.jugadas_legales():
                self.botones[i]['state'] = tk.NORMAL

            self.anuncio.master.wait_variable('sel_j')
            jugada = self.sel_j.get()
            juego.hacer_jugada(jugada)
            self.actualiza_tablero(jugada, color)

            ganancia = juego.terminal()
            if ganancia is not None:
                break

            self.anuncio['text'] = "Ahora juega Python"
            self.anuncio.update()
            for i in range(7):
                self.botones[i]['state'] = tk.DISABLED
                self.botones[i].update()

            jugada = minimax(juego, dmax=6, utilidad=utilidad_c4,
                             ordena_jugadas=ordena_jugadas,
                             transp=self.tr_ta)
            juego.hacer_jugada(jugada)
            self.actualiza_tablero(jugada, color_p)

            ganancia = juego.terminal()
            if ganancia is not None:
                break

        for i in range(7):
            self.botones[i]['state'] = tk.DISABLED

        str_fin = ("Ganaron las rojas" if ganancia > 0 else
                   "Ganaron las negars" if ganancia < 0 else
                   "Un asqueroso empate")
        self.anuncio['text'] = str_fin

    def actualiza_tablero(self, fila, color):
        for i in range(0, 41, 7):
            if self.can[i + fila].val == 0:
                self.can[i + fila].itemconfigure(self.cuadritos[i + fila],
                                                 fill=color)
                self.can[i + fila].val = 1 if color is 'red' else -1
                self.can[i + fila].update()
                break

    def arranca(self):
        self.app.mainloop()


if __name__ == '__main__':
    Conecta4GUI(tmax=10).arranca()
