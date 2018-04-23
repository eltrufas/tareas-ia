#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Rafael Alejandro Castillo Lopez'

import random
from collections import namedtuple

class Environment:
    '''
    Clase abstracta para ambientes, implementa cosas utiles
    '''
    def __init__(self, x0=None):
        if x0 is None:
            x0 = self.default_state()
        self._state = x0
        self.performance = 0

    def transition(self, action):
        '''
        Metodo publico para representar la transicion de un estado a otro
        '''
        if action not in self.legal_actions:
            raise ValueError("Accion ilegal")
        return self._transition(action)

    def _transition(self, action):
        '''
        Reemplaza este metodo para describir transiciones entre estados
        '''
        raise NotImplementedError

    @property
    def state(self):
        '''
        Propiedad de solo lectura que regresa el estado del modelo
        Regresar una copia o un objeto inmutable s'il vous plait
        '''
        return tuple(self._state)

    @property
    def legal_actions(self):
        '''
        Atributo que regresa un iterable con todas las acciones posibles
        para el estado del modelo
        '''
        return self.actions

    @property
    def percepts(self):
        '''
        Atributo para las percepciones que permite el modelo
        '''
        return self.state

    def __repr__(self):
        class_name = self.__class__.__name__
        return "{}(estado={}, desempeño={})".format(class_name,
                                                    self._state,
                                                    self.performance)
    @staticmethod
    def default_state():
        '''
        Metodo para construir un estado por defecto
        '''
        raise ValueError('Este ambiente no especifica un estado por default')


class TwoRoomEnvironment(Environment):
    '''
    Clase para el problema con dos cuartos y una aspiradora
    '''
    actions = ('go_a', 'go_b', 'clean', 'noop')

    def _transition(self, action):
        if action == 'noop':
            return
        else:
            self.performance -= 1

        if action == 'go_a':
            self._state[0] = 0
        elif action == 'go_b':
            self._state[0] = 1
        elif action == 'clean':
            position = self._state[0]
            self._clean_room(position)

    def _clean_room(self, room):
        self._state[room + 1] = 'clean'

    @property
    def percepts(self):
        position = self._state[0]
        return position, self._state[position + 1]

    @staticmethod
    def default_state():
        return [0, 'dirty', 'dirty']


class BlindTwoRoomEnvironment(TwoRoomEnvironment):
    @property
    def percepts(self):
        return self._state[0]


class StochasticTwoRoomEnvironment(TwoRoomEnvironment):
    '''
    Entorno para el mismo problema de dos cuartos con la diferencia de que
    existe una probablidad de 0.2 de que un cuarto no se limpie
    '''
    def _clean_room(self, room):
        if random.random() < 0.8:
            super()._clean_room(room)


class HouseState(namedtuple('HouseState', ['position', 'rooms'])):
    '''
    Representa un estado en el problema de seis cuartos
    '''
    def __str__(self):
        position, rooms = self
        dirty_rooms = sum(1 for x in rooms if x == 'dirty')
        return "Estado({} sucios, posicion: {})".format(dirty_rooms, position)


class HouseEnvironment(Environment):
    '''
    Modelo del ambiente de una casa de seis cuartos, para que una
    aspiradora robotica haga lo suyo

    La posicion actual se representa en el estado de acuerdo con este diagrama:
    -------
    |3|4|5|
    -------
    |0|1|2|
    -------
    '''
    actions = {'left', 'right', 'up', 'down', 'clean', 'noop'}

    def _transition(self, action):
        position, rooms = self._state

        if action == 'left':
            self.performance -= 1
            new_position = position - 1  if position % 3 \
                           else position
            self._state = HouseState(new_position, rooms)
        elif action == 'right':
            self.performance -= 1
            new_position = position + 1 if (position + 1) % 3 \
                           else position
            self._state = HouseState(new_position, rooms)
        elif action == 'up':
            self.performance -= 2 # es mas costoso moverse verticalmente
            self._state = HouseState(position + 3, rooms)
        elif action == 'down':
            self.performance -= 2
            self._state = HouseState(position - 3, rooms)
        elif action == 'clean':
            self.performance -= 1
            rooms[position] = 'clean'

    @property
    def state(self):
        current = self._state
        return HouseState(current.position, current.rooms[:]) #hacer copia

    @property
    def legal_actions(self):
        position, _ = self._state
        actions = set(self.actions)
        if position > 2:
            actions.remove('up')
        else:
            actions.remove('down')

        return tuple(actions)

    @property
    def percepts(self):
        position, rooms = self._state
        return position, rooms[position]

    @staticmethod
    def default_state():
        return HouseState(0, ['dirty' for _ in range(6)])


# Esto lo hice de mas porque no se leer
class BlindHouseEnvironment(HouseEnvironment):
    '''
    Entorno de los seis cuartos con la unica diferencia siendo que la
    percepcion es mas limitada (solo incluye la posicion)
    '''
    @property
    def percepts(self):
        position, _ = self._state
        return position


class RandomAgent:
    '''
    Agente aleatorio generico
    '''
    def __init__(self, environment):
        self.environment = environment

    def program(self, _):
        return random.choice(self.environment.legal_actions)

    def __repr__(self):
        return "RandomAgent"


class ReactiveHouseAgent:
    '''
    Clase que implementa un agente reactivo para el entorno de la
    aspiradora en la casa. Funciona haciendo un recorrido fijo y
    deteniendose a limpiar si encuentra un cuarto sucio, y
    deteniendose por completo cuando da una vuelta por toda la casa
    '''
    movement_sequence = ['right', 'right', 'up',
                         'down', 'left', 'left']
    route = [1, 2, 5, 0, 3, 4]
    def __init__(self):
        self.starting_position = None
        self.done = False

    def program(self, percerpts):
        position, room_state = percerpts

        next_room = self.route[position]

        if self.starting_position is None:
            self.starting_position = position

        if room_state == 'dirty':
            return 'clean'
        elif self.starting_position == next_room:
            self.done = True
            return 'noop'
        else:
            return self.movement_sequence[position]

    def __repr__(self):
        return "ReactiveHouseAgent(starting_position={})" \
            .format(self.starting_position)


# Esto tambien esta de mas
class BlindReactiveHouseAgent(ReactiveHouseAgent):
    '''
    Agente reactivo para el problema de los seis cuartos a ciegas,
    construido sobre el agente reactivo normal
    '''
    def __init__(self):
        super().__init__()
        self.cycle_state = 'clean'

    def program(self, position):
        if self.done:
            return 'noop'
        self.cycle_state = 'clean' if self.cycle_state == 'dirty' else 'dirty'
        return super().program((position, self.cycle_state))


class TwoRoomReactiveModelAgent:
    '''
    Agente reactivo para el problema de dos cuartos
    '''
    def __init__(self):
        self.starting_position = None

    def program(self, percepts):
        position, room_state = percepts
        if self.starting_position is None:
            self.starting_position = position

        return ('clean' if room_state == 'dirty' else
                'noop' if position != self.starting_position else
                'go_a' if position == 1 else 'go_b')

    def __repr__(self):
        return "TwoRoomReactiveModelAgent"


class BlindTwoRoomReactiveModelAgent(TwoRoomReactiveModelAgent):
    def __init__(self):
        super().__init__()
        self.cycle_state = 'clean'

    def program(self, position):
        if self.starting_position != position and self.cycle_state == 'dirty':
            return 'noop'

        self.cycle_state = 'clean' if self.cycle_state == 'dirty' else 'dirty'
        return super().program((position, self.cycle_state))




def simulate(environment, agent, steps=20):
    for _ in range(steps):
        p = environment.percepts
        a = agent.program(p)
        environment.transition(a)

        yield environment.state, p, a, environment.performance


def print_simulation(simulation):
    row_str = '|{0:4}|{2:10}|{3:30}|{4:17}|{1:12}|'
    print('-' * 79)
    print(row_str.format('paso', 'acción', 'desempeño',
                        'estado', 'percepción'))
    print('-' * 79)
    for step, result in enumerate(simulation):
        state, percept, action, performance = result
        print(row_str.format(step, action, performance, str(state), str(percept)))

    print('-' * 79)


def test_agent(agent, environment, steps=20):
    print('==Simulacion==\nEntorno: {}\nAgente: {}'.format(environment, agent))
    simulation = simulate(environment, agent)
    print_simulation(simulation)
    print('\n')


if __name__ == '__main__':

    # probar agente aleatorio
    environment = HouseEnvironment()
    agent = RandomAgent(environment)
    test_agent(agent, environment)

    # probar agente reactivo
    environment = HouseEnvironment()
    agent = ReactiveHouseAgent()
    test_agent(agent, environment)

    # probar agente reactivo a ciegas
    environment = BlindTwoRoomEnvironment()
    agent = BlindTwoRoomReactiveModelAgent()
    test_agent(agent, environment)

    # probar agente aleatorio a ciegas
    environment = BlindTwoRoomEnvironment()
    agent = RandomAgent(environment)
    test_agent(agent, environment)

    # probar agente aleatorio para dos cuartos estocastico
    environment = StochasticTwoRoomEnvironment()
    agent = RandomAgent(environment)
    test_agent(agent, environment)

    # probar agente reactivo para dos cuartos estocastico
    environment = StochasticTwoRoomEnvironment()
    agent = TwoRoomReactiveModelAgent()
    test_agent(agent, environment)
