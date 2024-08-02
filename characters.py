from itertools import combinations, permutations, product
from generator import RandomGenerator as RG         # Classe de parâmetros iniciais aleatórios
from effects import EffectManager as EM             # Classe de Buffs e Debuffs
from collections import defaultdict

import subprocess
import random
import numpy as np
import time
import json
# ----------------------------------------------------------------------------------------------------------- #
rg = RG()

class Hero:
    def __init__(self, base, parameters, team=0):
        self._turn = 0
        self._ally = []
        self._preset = parameters['preset'][2]
        self._skills = parameters['skills']
        self._countdowns = [0] * len(self._skills)
        self._base = self.__base(base)
        self._buffs = self.__buffs()
        self._debuffs = self.__debuffs()
        self._status = self.__status()
        self._turn_meter = 0.5

    def action(self):
        skills = [self._next()]
        if skills[1] > 0:
            skills.append(self._next())

        return {
            'team': self._team,
            'skills': skills
        }

    def _next(self):
        countdowns = self._update_countdowns()
        preset = self._preset
        skills = self._skills
        if self._turn == 1 and preset[0] != -1:
            self._countdowns[preset[0]] = skills[preset[0]][0]
            return skills[preset[0]]
        
        for el in preset[1:]:
            if countdowns[el] == 0:
                self._countdowns[el] = skills[el][0]
                return skills[el]
            else:
                time.sleep(0)
        print('Há um erro na lógica da função "next"')
        return -100
    
    def _update_countdowns(self):
        self._turn_meter = 0.0
        self._turn += 1
        self._countdowns = [c-1 if c > 0 else 0 for c in self._countdowns]
        return self._countdowns

    def __update_status(self):
        self._status = {
            'speed': self._base['speed'] * 0.0007 + self._buffs['speed']['rate'] + self._debuffs['speed']['rate']
        }

    def __base(self, base):
        return {
            'speed': base['speed']
        }
    
    def __buffs(self):
        return {
            'speed': {
                'rate': 0.0,
                'turn': 0
            }
        }
    
    def __debuffs(self):
        return {
            'speed': {
                'rate': 0.0,
                'turn': 0
            }
        }



class Team:
    def __init__(self):
        self._heroes = []
        return self

    def __getattr__(self, name):
        def method(*args, **kwargs):
            results = []
            for hero in self._heroes:
                hero_method = getattr(hero, name, None)
                if callable(hero_method):
                    result = hero_method(*args, **kwargs)
                    results.append(result)
                else:
                    print(f"{hero} does not have method {name}")
            return results
        return method
    
    def insert(self, *heroes):
        for hero in heroes:
            if isinstance(hero, Hero):
                self._heroes.append(hero)
        return self

    
