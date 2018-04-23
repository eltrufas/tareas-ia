#!/usr/bin/env python
# coding: utf-8


from busquedas_adversarios import JuegoSumaCeros2T
from busquedas_adversarios import minimax
import tkinter as tk


class Gato(JuegoSumaCeros2T):
    """
    El juego del gato para ilustrar los modelos de juegos

    """
    def __init__(self, jugador=1):
        """
        Inicializa el juego del gato

        """
        self.x0 = tuple(9 * [0])
        self.x = 9 * [0]
        self.historial = []
        self.jugador = 1

    def jugadas_legales(self):
        return (posicion for posicion in range(9) if self.x[posicion] == 0)

    def terminal(self):
        x = self.x
        if x[4] != 0 and (x[0] == x[4] == x[8] or x[2] == x[4] == x[6]):
            return x[4]
        for i in range(3):
            if x[3 * i] != 0 and x[3 * i] == x[3 * i + 1] == x[3 * i + 2]:
                return x[3 * i]
            if x[i] != 0 and x[i] == x[i + 3] == x[i + 6]:
                return x[i]
        if 0 not in self.x:
            return 0
        return None

    def hacer_jugada(self, jugada):
        self.historial.append(jugada)
        self.x[jugada] = self.jugador
        self.jugador *= -1

    def deshacer_jugada(self):
        jugada = self.historial.pop()
        self.x[jugada] = 0
        self.jugador *= -1


def juega_gato(jugador='X'):

    if jugador not in ['X', 'O']:
        raise ValueError("El jugador solo puede tener los valores 'X' o 'O'")
    juego = Gato()

    print("El juego del gato".center(60))
    print("las 'X' siempre empiezan".center(60))
    print("y tu juegas con {}".format(jugador).center(60))

    if jugador is 'O':
        jugada = minimax(juego)
        juego.hacer_jugada(jugada)

    acabado = False

    while not acabado:
        pprint_gato(juego.x)
        print("Escoge tu jugada (uno de los números que quedan en el gato)")

        try:
            jugada = int(input("Jugador {}: ".format(jugador)))
            print(jugada)
        except:
            print("¡No seas macana y pon un número!")
            continue
        if jugada < 0 or jugada > 8 or juego.x[jugada] != 0:
            print("¡No seas macana, pon un número válido!")
            continue

        juego.hacer_jugada(jugada)

        if juego.terminal() is not None:
            acabado = True
        else:
            jugada = minimax(juego)
            juego.hacer_jugada(jugada)
            if juego.terminal() is not None:
                acabado = True

    pprint_gato(juego.x)
    ganador = juego.terminal()
    if ganador == 0:
        print("UN ASQUEROSO EMPATE".center(60))
    elif (ganador < 0 and jugador is 'X') or (ganador > 0 and jugador is 'O'):
        print("¡Gané! ¡Juar, juar, juar!, ¿Quieres jugar otra vez?".center(60))
    else:
        print("Ganaste, bye.")
    print("\n\nFin del juego")


def pprint_gato(x):
    y = [('X' if x[i] > 0 else 'O' if x[i] < 0 else str(i))
         for i in range(9)]
    print(" {} | {} | {} ".format(y[0], y[1], y[2]).center(60))
    print("---+---+---".center(60))
    print(" {} | {} | {} ".format(y[3], y[4], y[5]).center(60))
    print("---+---+---".center(60))
    print(" {} | {} | {} ".format(y[6], y[7], y[8]).center(60))


class GatoTK:
    def __init__(self, escala=2):

        self.app = app = tk.Tk()
        self.app.title("El juego del gato")
        self.L = L = int(escala) * 50

        tmpstr = "Escoge, X siempre empiezan"
        self.anuncio = tk.Message(app, bg='white', borderwidth=1,
                                  justify=tk.CENTER, text=tmpstr,
                                  width=3 * L)
        self.anuncio.pack()

        barra = tk.Frame(app)
        barra.pack()
        botonX = tk.Button(barra,
                           command=lambda x=True: self.jugar(x),
                           text='(re)iniciar con X')
        botonX.grid(column=0, row=0)
        botonO = tk.Button(barra,
                           command=lambda x=False: self.jugar(x),
                           text='(re)iniciar con O')
        botonO.grid(column=1, row=0)

        ctn = tk.Frame(app, bg='black')
        ctn.pack()
        self.tablero = [None for _ in range(9)]
        self.textos = [None for _ in range(9)]
        letra = ('Helvetica', -int(0.9 * L), 'bold')
        for i in range(9):
            self.tablero[i] = tk.Canvas(ctn, height=L, width=L,
                                        bg='light grey', borderwidth=0)
            self.tablero[i].grid(row=i // 3, column=i % 3)
            self.textos[i] = self.tablero[i].create_text(L // 2, L // 2,
                                                         font= letra, text=' ')
            self.tablero[i].val = 0
            self.tablero[i].pos = i

    def jugar(self, primero):
        juego = Gato()

        if not primero:
            jugada = minimax(juego)
            juego.hacer_jugada(jugada)

        self.anuncio['text'] = "A ver de que cuero salen más correas"
        for _ in range(9):
            self.actualiza_tablero(juego.x)
            jugada = self.escoge_jugada(juego)
            juego.hacer_jugada(jugada)
            ganador = juego.terminal()
            if ganador is not None:
                break
            jugada = minimax(juego)
            juego.hacer_jugada(jugada)
            ganador = juego.terminal()
            if ganador is not None:
                break

        self.actualiza_tablero(juego.x)
        finstr = ("UN ASQUEROSO EMPATE, aggggg" if ganador == 0 else
                  "Ganaste, bye"
                  if (ganador > 0 and primero) or (ganador < 0 and not primero)
                  else "¡Gané¡  Juar, juar, juar.")
        self.anuncio['text'] = finstr
        self.anuncio.update()

    def escoge_jugada(self, juego):
        jugadas_posibles = list(juego.jugadas_legales())
        if len(jugadas_posibles) == 1:
            return jugadas_posibles[0]

        seleccion = tk.IntVar(self.tablero[0].master, -1, 'seleccion')

        def entrada(evento):
            evento.widget.color_original = evento.widget['bg']
            evento.widget['bg'] = 'grey'

        def salida(evento):
            evento.widget['bg'] = evento.widget.color_original

        def presiona_raton(evento):
            evento.widget['bg'] = evento.widget.color_original
            seleccion.set(evento.widget.pos)

        for i in jugadas_posibles:
            self.tablero[i].bind('<Enter>', entrada)
            self.tablero[i].bind('<Leave>', salida)
            self.tablero[i].bind('<Button-1>', presiona_raton)

        self.tablero[0].master.wait_variable('seleccion')

        for i in jugadas_posibles:
            self.tablero[i].unbind('<Enter>')
            self.tablero[i].unbind('<Leave>')
            self.tablero[i].unbind('<Button-1>')
        return seleccion.get()

    def actualiza_tablero(self, x):
        for i in range(9):
            if self.tablero[i].val != x[i]:
                self.tablero[i].itemconfigure(self.textos[i],
                                              text=' xo'[x[i]])
                self.tablero[i].val = x[i]
                self.tablero[i].update()

    def arranca(self):
        self.app.mainloop()


if __name__ == '__main__':
    # juega_gato('X')
    GatoTK().arranca()
