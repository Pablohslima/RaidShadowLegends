import unittest
import time
import inspect
from collections import defaultdict

class EffectManager:
    def __init__(self):
        self._positive = TypeEffect('positive')
        self._negative = TypeEffect('negative')

    def __getitem__(self, stats):
        return self.__rate(stats)

    @property
    def value(self):
        return {
            'positive': self._positive.value,
            'negative': self._negative.value
        }
    @property
    def positive(self):
        return self._positive
    
    @property
    def negative(self):
        return self._negative
    
    def insert(self, *effects): # dict {'stats', 'rate', 'turn', 'new', 'protected'}
        for effect in effects:
            if effect['rate'] > 0.0:
                self._positive.insert(effect)
            elif effect['rate'] < 0.0:
                self._negative.insert(effect)
            else:
                print(f'Invalid Effect: {effect}')
        return self

    def start(self): # Início do turno
        self._negative.reduce_all()
        return self

    def end(self): # Fim do turno
        self._positive.reduce_if(('new', False, True))
        self._positive.to_old()
        return self
    
    def print(self):
        self._positive.print()
        self._negative.print()
        return self

    def __rate(self, effect): # Buff e Debuff somados
        rate = 1.0
        rate *= self._positive[effect]
        rate *= self._negative[effect]
        return round(rate, 5)

class TypeEffect:
    def __init__(self, type):
        self._type = type
        self._effects = {}
        self._new = set()
        self._print = False

    def __getitem__(self, stats):
        rate = 1.0 + self._effects[stats]['rate']
        return round(rate, 5)

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._effects

    def extend_all(self):
        for effect in self._effects.values():
            effect['turn'] += 1
        return self.__print()
    
    def extend_if(self, *args):  # args: tuples (key, val, cond)
        for effect in self._effects.values():
            if all(
                (key in effect and (effect[key] == val if cond else effect[key] != val))
                for key, val, cond in args
            ):
                effect['turn'] += 1
        return self.__print()

    def reduce_all(self):
        to_delete = []
        for key, effect in self._effects.items():
            effect['turn'] -= 1
            if effect['turn'] == 0:
                to_delete.append(key)
        for key in to_delete:
            del self._effects[key]
        return self.__print()
    
    def reduce_if(self, *args):  # args: tuples (key, val, cond)
        to_delete = []
        for key, effect in self._effects.items():
            if all(
                (key in effect and (effect[key] == val if cond else effect[key] != val))
                for key, val, cond in args
            ):
                effect['turn'] -= 1
                if effect['turn'] == 0:
                    to_delete.append(key)
        for key in to_delete:
            del self._effects[key]
        return self.__print()

    def to_old(self):
        for effect in self._new:
            self._effects[effect]['new'] = False

        self._new = set()
        return self.__print()

    def clear(self):
        self._effects.clear()
        return self.__print()

    def insert(self, *effects): # dict {'stats', 'rate', 'turn', 'new', 'protected'}
        for effect in effects:
            if isinstance(effect, dict):
                if len(self._effects) == 10 and effect['stats'] not in self._effects:
                    continue
                self.__insert(effect)
            else:
                print(f'Invalid Effect Format: {effect}')
        return self

    def print(self):
        self._print = not self._print
        print(f'{self.type} -> Modo print {"Ativo" if self._print else "Inativo"}!')
        return self

    def __insert(self, effect): # dict {'stats', 'rate', 'turn', 'new', 'protected'}
        # Chaves padrão com seus valores iniciais
        default_values = {'rate': 0.0, 'turn': 0, 'new': True, 'protected': False}
        
        # Mesclar o efeito recebido com os valores padrão
        current = self._effects.setdefault(effect['stats'], default_values.copy())
        
        # Update if the new rate is greater or if the rate is the same but the turn count is higher
        if (
            abs(effect['rate']) > abs(current['rate'])
            or (
                abs(effect['rate']) == abs(current['rate']) and effect['turn'] >= current['turn']
            )
        ):
            current['rate'] = effect['rate']
            current['turn'] = effect['turn']
            current['new'] = effect.get('new', True)
            current['protected'] = effect.get('protected', False)
            if current['new']:
                self._new.add(effect['stats'])

        # Print a atualização dos itens
        return self.__print()

    def __print(self):
        if self._print:
            # Obtém o quadro atual e o quadro do chamador
            current_frame = inspect.currentframe()
            caller_frame = current_frame.f_back
            caller_function_name = caller_frame.f_code.co_name.center(10)

            # Formata a mensagem para impressão
            message = f"{self._type} -> {caller_function_name} -> {self._effects}"
            
            # Print the message
            print(message)
            
        return self

if __name__ == '__main__':

    te = TypeEffect('positive')
    em = EffectManager()
    em.print().insert(
        {'stats': 'speed', 'rate': 0.15, 'turn': 4, 'new': True, 'protected': False}
    ).start().end()
    em.positive.reduce_all()
    em.insert(
        {'stats': 'speed', 'rate': -0.30, 'turn': 3, 'new': True, 'protected': False}
    )
    em.negative.extend_all()
    print("Propriedades:")
    print('\titem, value', '->', em['speed'], em.value)
    em.positive.clear()
    em.positive.clear()
    em.print()
