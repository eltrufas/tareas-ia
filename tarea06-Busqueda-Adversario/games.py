from collections import namedtuple
from time import perf_counter
import random


class Position(namedtuple('Position', ['board', 'player'])):
    @property
    def terminal(self):
        '''
        Regresa el jugador que ganó, o 0 si el juego esta inconcluso.
        '''
        raise NotImplementedError('Game class must implement '
                                  'the status method')

    @property
    def legal_moves(self):
        raise NotImplementedError('Game class must implement '
                                  'the legal_moves method')

    def make_move(self, play):
        raise NotImplementedError('Game class must implement '
                                  'the _make_play method')

    @property
    def child_nodes(self):
        return (self.make_move(play) for play in self.legal_moves)

    @property
    def tag(self):
        '''
        Regresa una etiqueta inmutable unica a esta posición, para ser usada
        como llave en tablas de transposición y cosas así. Solo deberia
        sobrecargarse si el estado de juego es mutable (En la mayoria de los
        casos esto no es necesario).
        '''
        return self

    @staticmethod
    def __default_state__():
        raise NotImplementedError('Game class must implement the'
                                  '__default_state__ method')


inf = float('infinity')

TransTableEntry = namedtuple('TransTableEntry',
                             ['flag', 'depth', 'value', 'move'])


class Negamax:
    def __init__(self, utility=None, order_moves=None, max_depth=10):
        if utility is None:
            def utility(pos):
                return pos.terminal
        if order_moves is None:
            def order_moves(position):
                p = list(position.legal_moves)
                random.shuffle(p)
                return p

        self.utility = utility
        self.order_moves = order_moves
        self.max_depth = 10

    def __call__(self, pos, max_time=10):
        branching_factor = len(list(pos.legal_moves))
        self.trans_table = {}
        start_time = perf_counter()
        for depth in range(2, self.max_depth):
            local_start = perf_counter()
            score, move = self.nega_run(pos, depth, -inf, inf, pos.player)
            local_end = perf_counter()

            if (branching_factor * (local_end - local_start) >
                    start_time + max_time - local_end):

                return move
        return move

    def nega_run(self, pos, depth, alpha, beta, player):
        original_alpha = alpha

        entry = self.trans_table.get(pos.hashable_pos())
        if entry is not None and entry.depth >= depth:
            if entry.flag == 'exact':
                return entry.value, entry.move
            if entry.flag == 'lower_bound':
                alpha = max(alpha, entry.value)
            elif entry.flag == 'upper_bound':
                beta = min(beta, entry.value)
            if alpha >= beta:
                return entry.value, entry.move

        if depth == 0 or pos.terminal:
            return player * self.utility(pos), None

        moves = self.order_moves(pos)
        if entry:
            moves.remove(entry.move)
            moves.insert(0, entry.move)

        best_score = -inf
        best_move = None
        for move in moves:
            new_pos = pos.make_move(move)
            v, m = self.nega_run(new_pos, depth-1, -beta, -alpha, -player)
            v = -v

            if best_score < v:
                best_score = v
                best_move = move

            if alpha < v:
                alpha = v
                if alpha > beta:
                    break

        flag = ('upper_bound' if best_score <= original_alpha else
                'lower_bound' if best_score >= beta else 'exact')

        entry = TransTableEntry(flag, depth, best_score, best_move)
        self.trans_table[pos.hashable_pos()] = entry

        return best_score, best_move
