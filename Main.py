"""
# ============================= [ Informações ] ============================= #
# Turn Meter Max: 100
# Turn Meter Fill Rate: 0.07
# Turn Meter to Turn: 100/0.07 == 1428.57143
# Tick = Vel/TMT, exemplo: Vel == 190 Tick = 190/1428.57143 == 0.132299

# ============================== [ Entradas ] ============================== #
    [] Herois
        [] Base Speed (80-150)
        [] Skills (3) -> 4788
            [] Extended
            [] Rate (0-90)(%5)
            [] Turn Meter Fill (5-100)(5%) 
            [] Countdown (1-5)
        [] Preset (3)
            [] Opener
            [] Off
            [] First
            [] Second
            [] Third

            Parametro 1:
            parametros = [1, 2, 3]
            opções = {
                0: Nenhuma
                2: Opener
                3: Off
                4: OpenerOff
            }
                * Cada parametro pode ter apenas 1 opção
                * Todos parametros podem ter a opção 0
                * No maxímo 1 parametro pode ter a opção 1
                * No máximo 2 parametros podem ter a opção 2
                * O parametro 3 represanta os parametros 1 e 2 ao mesmo tempo.
                1: opção
                1: opção
                2: opção

            Parametro 2:
                0: [0, 1, 2, 3]
                1: [0, 1, 2, 3]
                2: [0, 1, 2, 3]


# =============================== [ Treino ] =============================== #
[] Criar Classe Hero(base_speed, preset)
    -> nome
    -> turn_meter
    -> presets

[] Criar Classe Speed
    -> base
    -> true
    -> buff
    -> debuff
    -> tick_rate
[] Criar Classe Skill
[] Criar Classe PreSet
[] Criar Classe Time

=====================================================================================================================================
"""

import numpy as np
import itertools
import time

def generate_combinations(parameters):
    values = []

    for param in parameters:
        param_type = param['type']
        range_values = param['range']
        increment = param['increment']

        if param_type == int:
            values.append(np.arange(range_values[0], range_values[1] + 1, increment).tolist())
        elif param_type == float:
            values.append(np.round(np.arange(range_values[0], range_values[1] + increment, increment), 2).tolist())

    combinations = list(itertools.product(*values))

    return combinations

parameters_combinations = {
    'skill': {
        'extend': {'type': int, 'range': (0, 1), 'increment': 1},
        'countdown': {'type': int, 'range': (0, 5), 'increment': 1},
        'rate': {'type': float, 'range': (0.0, 0.9), 'increment': 0.05},
        'fill': {'type': float, 'range': (0.0, 1.0), 'increment': 0.05}
    },
    'preset': {
        1: {'type': int, 'range': (0, 1), 'increment': 1},
        2: {'type': int, 'range': (0, 3), 'increment': 1},
        3: {'type': int, 'range': (0, 3), 'increment': 1},
        4: {'type': int, 'range': (0, 3), 'increment': 1}
    }
}

def preSetIsValid(combinations, lenght):
    isValid = []
    l = lenght - 1
    for comb in combinations:
        c = comb[:l]
        if c.count(1) > 1 or c.count(2) > l or c.count(3) > l:
            continue
        if 1 in c and 3 in c:
            continue
        isValid.append(c)
    return isValid


skillsValues = generate_combinations(parameters_combinations['preset'].values())
preSetsValues = {
    1: preSetIsValid(skillsValues, 2),
    2: preSetIsValid(skillsValues, 3),
    3: preSetIsValid(skillsValues, 4),
    4: preSetIsValid(skillsValues, 5)
}

for r in result:
    print(r)
    time.sleep(0.1)
"""
                * Cada parametro pode ter apenas 1 opção
                * Todos parametros podem ter a opção 0
                * No maxímo 1 parametro pode ter a opção 1
                * No máximo 2 parametros podem ter a opção 2
                * O parametro 3 represanta os parametros 1 e 2 ao mesmo tempo.
"""