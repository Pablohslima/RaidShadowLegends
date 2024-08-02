class TypeEffect:
    def __init__(self, type):
        self._type = type
        self._effects = {}

    def __getitem__(self, stats):
        rate = 1.0 + self._effects[stats]['rate']
        return round(rate, 5)

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._effects

    def extendAll(self):
        effects = self._effects
        for effect in effects.values():
            effect['turn'] += 1
        return self
    
    def extendIf(self, *args): # tuple(new, True, True)
        effects = self._effects
        for effect in effects:
            if all(
                (key in effect and (effect[key] == val if cond else effect[key] != val))
                for key, val, cond in args
            ):
                effect['turn'] += 1
        return self

    def reduceAll(self):
        effects = self._effects
        for effect in effects.values():
            effect['turn'] -= 1
            if effect['turn'] == 0:
                del self._effects[effect]
        return self
    
    def reduceIf(self, *args): # tuple(new, True, True)
        effects = self._effects
        for effect in effects:
            if all(
                (key in effect and (effect[key] == val if cond else effect[key] != val))
                for key, val, cond in args
            ):
                effect['turn'] -= 1
                if effect['turn'] == 0:
                    del self._effects[effect]
        return self

    def change_all(self, key='new', value=False):
        effects = self._values
        for effect in effects.values():
            effect[key] = value
        return self

    def clear(self):
        self._effects.clear()
        return self

    def insert(self, *effects): # tuple(stats, value, turn)
        for effect in effects:
            self.__insert(effect)
        return self

    def __insert(self, effect): # tuple(stats, value, turn)
        stats, rate, turns = effect
        current = self._effects.setdefault(stats, {'rate': 0.0, 'turn': 0, 'new': True})
        if abs(rate) >= abs(current['rate']) and turns >= current['turn']:
            current.update({'rate': rate, 'turn': turns, 'new': True})
        return self