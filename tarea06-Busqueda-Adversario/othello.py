#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustes mismos, con jugador inteligente

"""
from games import Position, Negamax
from itertools import product
import numpy as np
import random

__author__ = 'Rafael Castillo'


# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------
class ReversiPosition(Position):
    directions = set(product(*((-1, 0, 1),) * 2)) - {(0, 0)}

    @property
    def legal_moves(self):
        moves = list(self.moves_for(self.player))
        return moves if moves else ['pass']

    def moves_for(self, player):
        return (coord for (coord, _) in np.ndenumerate(self.board)
                if self.is_legal(coord, player))

    def is_legal(self, coord, player):
        if self.board[coord]:
            return False
        for walk in (self.walk(d, coord, player) for d in self.directions):
            for _ in walk:
                return True
        return False

    def make_move(self, move):
        if move == 'pass':
            return ReversiPosition(self.board, self.player)

        new_board = np.copy(self.board)

        new_board[move] = self.player
        for walk in (self.walk(d, move, self.player) for d in self.directions):
            for coord in walk:
                new_board[coord] = self.player

        return ReversiPosition(new_board, -self.player)

    def walk(self, direction, coord, player):
        '''
        Regresa las fichas en directiom que player voltearia si colocara en
        coord. Espero que esa explicación haya servido.
        '''
        dx, dy = direction
        xi, yi = coord
        xi, yi = xi + dx, yi + dy
        walk = []
        while self.valid_coord(xi, yi):
            if not self.board[xi, yi]:
                break
            if self.board[xi, yi] == player:
                return walk
            walk.append((xi, yi))

            xi, yi = xi + dx, yi + dy

        return []

    @staticmethod
    def valid_coord(x, y):
        # Regresa si una coordenada esta dentro del tablero.
        return 0 <= x < 8 and 0 <= y < 8

    @property
    def terminal(self):
        if (not np.sum(self.board == 0) or
                (not sum(1 for _ in self.moves_for(1)) and
                 not sum(1 for _ in self.moves_for(1)))):
            return max((-1, 1), key=lambda p: np.sum(self.board == p))
        return 0

    def hashable_pos(self):
        '''
        Uso esto porque no puedo usar un arreglo de numpy como llave de
        diccionario.
        '''
        return self.board.tostring(), self.player

    def pprint(self, moves={}):
        '''
        Imprime el otelo con una apariencia decentona. El resultado me lo robé
        de la interfaz del dui, pero la implementación es mayormente original
        '''
        header = ('    A   B   C   D   E   F   G   H\n'
                  '  ┌───┬───┬───┬───┬───┬───┬───┬───┐')

        def pick_symbol(val, y, x):
            move = (y, x)
            return (moves[move] if move in moves else
                    '●' if val == 1 else '○' if val == -1 else ' ')

        filler = '\n  ├───┼───┼───┼───┼───┼───┼───┼───┤\n'
        rows = filler.join([str(i) + ' │ ' + ' │ '.join([pick_symbol(val, i, j)
                                                         for j, val
                                                         in enumerate(row)]) +
                            ' │' for i, row in enumerate(self.board)])

        print(header)
        print(rows)
        print('  └───┴───┴───┴───┴───┴───┴───┴───┘\n')

        print('Conteo: {} ●, {} ○'.format(np.sum(self.board == 1),
                                          np.sum(self.board == -1)))


''' FUNCIONES DE UTILIDAD '''

SQUARE_SCORE = np.array([[9, 1, 3, 3, 3, 3, 1, 9],
                         [1, 1, 1, 1, 1, 1, 1, 1],
                         [3, 1, 1, 1, 1, 1, 1, 3],
                         [3, 1, 1, 1, 1, 1, 1, 3],
                         [3, 1, 1, 1, 1, 1, 1, 3],
                         [3, 1, 1, 1, 1, 1, 1, 3],
                         [1, 1, 1, 1, 1, 1, 1, 1],
                         [9, 1, 3, 3, 3, 3, 1, 9]])


def corner_utility(position):
    corners = position.board[[0, 0, -1, -1], [0, -1, 0, -1]]
    max_corners = len(corners == 1)
    min_corners = len(corners == -1)

    return ((max_corners - min_corners) / (max_corners + min_corners)
            if (max_corners + min_corners) else 0)


def bad_utility(position):
    return np.sum(position.board)


def static_utility(position):
    return np.sum(np.multiply(SQUARE_SCORE, position.board))


def hybrid_utility(position):
    max_chips = np.sum(position.board == 1)
    min_chips = -np.sum(position.board == -1)
    total_chips = max_chips + min_chips

    if total_chips < 48:
        return static_utility(position)
    else:
        return (max_chips - min_chips) / total_chips


def simple_order(position):
    moves = list(position.legal_moves)
    moves.sort(key=lambda m: SQUARE_SCORE[m], reverse=(position.player == 1))
    return moves


def make_reversi():
    board = np.zeros((8, 8), dtype=np.int8)
    board[3, [3, 4]] = [1, -1]
    board[4, [3, 4]] = [-1, 1]
    return ReversiPosition(board, 1)


'''
PRECAUCION: LAS SIGUIENTES ~100 LINEAS SON COSAS DE LA INTERFAZ.
'''


def make_alg_notation(move):
    if move == 'pass':
        return 'Pasar'
    y, x = move
    return '{}{}'.format(chr(ord('A') + x), y)


def human_player(game):
    moves = {move: chr(ord('a') + i)
             for i, move in enumerate(game.legal_moves)}
    rev_moves = {value: key for key, value in moves.items()}
    prompt = ' '.join(["{0}: {1}".format(c, make_alg_notation(move))
                       for move, c in moves.items()])

    print(moves.values())

    game.pprint(moves)

    print('Jugadas legales: ')
    print(prompt)
    print('Escoge una opción: ')
    choice = input()
    if choice in rev_moves:
        print('Escogiste jugar en {}'
              .format(make_alg_notation(rev_moves[choice])))
        return rev_moves[choice]

    print('Entrada invalida, intenta de nuevo')

    return human_player(game)


# Solo dios puede juzgarme
move_descriptions = [', ¡un movimiento excelente!',
                     '. ¡Hasta un bebé lo pudo ver venir!',
                     '. ¿Qué está pensando?',
                     '. He visto mejores.',
                     '. ¿Será este su fin?',
                     '. Una jugada elegante sin duda.',
                     '. La situación se calienta.',
                     '. Se siente la tensión en el aire',
                     '. No sé que decir.',
                     '. Una jugada espectacular',
                     '.']


def ai_pretty_wrapper(ai):
    '''
    Decorador sencillo que solo imprime texto sobre la movida de la maquina
    '''
    def wrapped(game):
        game.pprint()
        print('La computadora esta pensando. '
              'Esperemos que se le ocurra algo bueno.')

        move = ai(game)

        print('La computadora ha elegido jugar en {}{}'
              .format(make_alg_notation(move),
                      random.choice(move_descriptions)))

        return move

    return wrapped


def play(*players):
    game = make_reversi()

    next = 0
    while not game.terminal:
        next_player = players[next]

        move = next_player(game)
        game = game.make_move(move)

        next = (next + 1) % len(players)

    game.pprint()

    result = game.terminal
    if result == 1:
        print('Ganaron las blancas!')
    elif result == -1:
        print('Ganaron las negras!')


if __name__ == '__main__':
    ai = ai_pretty_wrapper(Negamax(hybrid_utility))
    print('!' * 80)
    print('Buen dia. Este es el otelo. Si quieres cambiar quien empieza o \n'
          'ponerlo para que dos maquinas se agarren a fregazos, vas a tener \n'
          'que cambiar el código')
    print('¡' * 80)

    '''
    Afortunadamente cambiar quienes juegan es sencillo. Ahorita esta puesto
    para jugar un humano contra un jugador de computadora:
    '''
    play(human_player, ai)

    '''
    Pero fácilmente  podría haber dos personas jugando entre sí (¿por qué?)

    play(human_player, human_player)


    O incluso dos maquinas (util para comparar utilidades!)

    other_ai = ai_pretty_wrapper(Negamax(dumb_utility))

    play(ai, other_ai)

    '''
