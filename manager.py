import unittest
import time
from collections import defaultdict

class EffectManager:
    def __init__(self):
        self._positive = {}
        self._negative = {}

    def __getitem__(self, stats):
        return self.__rate(stats)

    @property
    def all(self):
        return {
            'positive': self._positive,
            'negative': self._negative
        }

    def start(self):
        return self.reduce('negative')

    def end(self):
        self.__change_all('positive', 'new', False)
        return self.reduce('positive')

    def extend(self, effect_type='positive'):
        effects = self.__get_effects(effect_type)
        if effects is not None:
            for effect in effects.values():
                effect['turn'] += 1
            return self
        return None

    def reduce(self, effect_type='positive'):
        effects = self.__get_effects(effect_type)
        if effects is not None:
            for effect in effects.values():
                effect['turn'] -= 1
            return self
        return None

    def clear(self, effect_type='positive'):
        effects = self.__get_effects(effect_type)
        if effects is not None:
            effects.clear()
            return self
        return None

    def add(self, *effects):
        for effect in effects:
            effect_name, rate, turns = effect
            effect_type = self._positive if rate > 0 else self._negative

            current_effect = effect_type.setdefault(effect_name, {'rate': 0.0, 'turn': 0, 'new': True})

            if abs(rate) >= abs(current_effect['rate']) and turns >= current_effect['turn']:
                current_effect.update({'rate': rate, 'turn': turns, 'new': True})

        return self
    
    def __rate(self, stats):
        rate = 1.0
        rate *= 1 + self._positive.get(stats, {'rate': 0.0})['rate']
        rate *= 1 + self._negative.get(stats, {'rate': 0.0})['rate']
        return round(rate, 5)

    def __change_all(self, effect_type='positive', key='new', value=False):
        effects = self.__get_effects(effect_type)
        if effects is not None:
            for effect in effects.values():
                effect[key] = value
        return self.all

    def __get_effects(self, effect_type):
        if effect_type not in {'positive', 'negative'}:
            raise ValueError("Invalid effect_type. Expected 'positive' or 'negative'.")
        return getattr(self, f'_{effect_type}')

