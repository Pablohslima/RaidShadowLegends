"""
# ================================ [ Ideia ] ================================ #
    * No jogo Raid: Shadow Legends, saber como montar e ajustar um time é muito vantajoso. Tendo isso em vista,
    pretendemos desenvolver uma rede neural capaz de nos auxiliar nesse aspecto do jogo.
    *Entradas: 
        * Velocidade do Boss
        * Para cada herói a rede neural deve receber:
            * 5 Skills.
            * 1 Preset, que indica a ordem que as skills serão usadas.
            * 1 Occurrence, que indica quantas vezes o herói deverá agir antes do Boss atacar no turno.
    * Para cada herói a rede neural deve fornecer como saída:
        * Velocidades verdadeiras necessárias para que a Occurrence seja cumprida.

# ============================ [ Planejamento ] ============================= #
1. [ ] Criar uma simulação do jogo.

2. [ ] Criar DataBase com informações turno a turno de uma partida.
    ** Detalhes:
        * Um turno termina quando o Boss ataca.
    [x] Criar função que retorne Skill genérica.
        [x] Criar DabaBase com todas combinações utilizadas nas Skills genéricas.
        [x] Alterar estratégia.
        [x] Criar função que retorne valores aleatórios para skills a1 e a2+.
    [x] Criar função que retorne Preset genérico.
        [x] Criar DataBase com todas combinações utilizadas nos Presets.
        [x] Alterar estratégia.
        [x] Criar função que retorne valores aleatórios para Presets.
    [x] Criar função que retorne 1 Preset, 1 Skill A1 e 4 Skills A2 aleatórias e sem repetição.

3. [ ] Criar uma função capaz de definir se uma partida cumpre ou não a ocurrence definida.

# ============================= [ Informações ] ============================= #
# Turn Meter Max: 100
# Turn Meter Fill Rate: 0.07
# Turn Meter to Turn: 100/0.07 == 1428.57143
# Tick = Vel/TMT, exemplo: Vel == 190 Tick = 190/1428.57143 == 0.132299

# ============================== [ Entradas ] ============================== #
    [ ] Herois
        [ ] Base Speed (80-150)

        [x] Skills
            [x] Countdown           ->  [0]         [1-7]
            [x] Extra Turn          ->  [0]         [0-1]
            [x] Buff Extend         ->  [0]         [0-1]
            [x] Buff Turns          ->  [0]         [0-3]
            [x] Speed Rate          ->  [0]         [0-0.3]
            [x] Turn Meter Fill     ->  [0-0.1]     [0-1.0]

        [x] Preset: Restrictions + Priorities -> 2.304
            [x] None
            [x] Opener
            [x] Block
            [x] OpenerBlock
            [x] First Priority
            [x] Second Priority
            [x] Third Priority
            [x] Forth Priority
            [x] Fifth Priority
=====================================================================================================================================
"""
from itertools import combinations, permutations, product
from generator import RandomGenerator as RG

import subprocess
import random
import numpy as np
import time
import json
# ----------------------------------------------------------------------------------------------------------- #
rg = RG()

# ----------------------------------------------------------------------------------------------------------- #
def prtit(iterable, group_size=5): # PRINT A iterable IN GROUPS OF group_size
    """
    Imprime elementos do iterável em grupos de tamanho especificado.

    Args:
        iterable: Um iterável contendo os elementos a serem impressos.
        group_size: Um inteiro representando o número de elementos por grupo.
    """
    # Converte o iterável em uma lista para permitir o fatiamento
    iterable_list = list(iterable)
    
    # Itera sobre a lista em passos de 'group_size'
    for i in range(0, len(iterable_list), group_size):
        # Fatia a lista para obter o grupo atual
        group = iterable_list[i:i + group_size]
        # Imprime o grupo
        print(group)
"""
    Hero.action
        zerar turne metter
        reduzir countdown de todas skills
        reduzir duraçao dos buff ativos
        identificar próxima skill
        usar skill
        atualizar countdown daquela skill
        retornar informaçoes a serem atualizadas no time todo. nao esquecer do turno extra.

"""
class Hero:
    def __init__(self, base, parameters, team=0):
        self._turn = 0
        self._team = team
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


class StatusEffectManager:
    def __init__(self):
        self._active = {}

    def extend(self, effect_type='positive'): # Ex: negative|positive
        active = self._active
        for effect in active:
            if effect_type in effect:
                effect[effect_type]['turn'] += 1
        return active

    def reduce(self, effect_type='positive'): # Ex: negative|positive
        active = self._active
        for effect in active:
            if effect_type in effect:
                if effect[effect_type]['turn'] == 1:
                    del effect[effect_type]
                else:
                    effect[effect_type]['turn'] -= 1
        return active

    def clean(self, effect_type='positive'): # Ex: negative|positive
        active = self._active
        for effect in active:
            if effect_type in effect:
                del effect[effect_type]
        return active

    def add(self, *effects):  # Ex: ('speed', +-0.3, 2)
        active = self._active
        for effect in effects:
            effect_name, rate, turns = effect
            effect_type = 'positive' if rate > 0.0 else 'negative'

            # Usar setdefault para garantir que as chaves existam
            effect_data = active.setdefault(effect_name, {})\
                .setdefault(effect_type, {'rate': 0.0, 'turn': 0, 'new': True})

            # Atualizar somente se as novas condições forem melhores
            if abs(rate) >= abs(effect_data['rate']) and turns >= effect_data['turn']:
                effect_data.update({'rate': rate, 'turn': turns, 'new': True})
        print(self._active)
        return active

    def _sum(self):
        active = self._active
        for effect in active:
            value = 0.0
            positivo = effect.get('positivo', 0) + 1
            negativo = effect.get('negativo', 0) + 1


active = {
    'speed': {
        'positivo': {
            'rate': 0.3
        },
        'negativo': {
            'rate': -0.3
        }
    }
}

par = {
    "preset": [
        (0, 0, 0, 1, 2),
        (1, 5, 3, 4, 2),
        (3, 1, 3, 2, 0)
    ],
    "skills": [
        (0, 0, 0, 0, 0.0, 0.0),
        (2, 1, 1, 1, 0.15, 0.2),
        (3, 0, 0, 2, 0.15, 0.4),
        (4, 0, 0, 1, 0.15, 0.3),
        (6, 0, 1, 1, 0.3, 1.0)
    ]
}

h = Hero(190, par)

print(par['preset'][2])
print(par['skills'])

for i in range(1, 20):
    print('Turno:', i, '->', 'Skill:', h.next())

"""
    "preset": [
        (0, 2, 2, 0, 2),
        (1, 2, 5, 4, 3),
        (-1, 3, 0)
    ]
"""




