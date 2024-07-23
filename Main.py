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

from generator import rvcg as gen, gen_test

import numpy as np
from itertools import combinations, permutations, product
import subprocess
import random
import time
import json
# ----------------------------------------------------------------------------------------------------------- #

def pplist(iterable, group_size=5):
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

gen_test()
