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
        [x] Alterar estratégia
        [x] Criar função que retorne valores aleatórios para skills a1 e a2+.
    [x] Criar função que retorne Preset genérico.
        [x] Criar DataBase com todas combinações utilizadas nos Presets.
        [x] Alterar estratégia
        [x] Criar função que retorne valores aleatórios para Presets.
3. [ ] Criar uma função capaz de definir se uma partida cumpre ou não a ocurrence definida.

# ============================= [ Informações ] ============================= #
# Turn Meter Max: 100
# Turn Meter Fill Rate: 0.07
# Turn Meter to Turn: 100/0.07 == 1428.57143
# Tick = Vel/TMT, exemplo: Vel == 190 Tick = 190/1428.57143 == 0.132299

# ============================== [ Entradas ] ============================== #
    [ ] Herois
        [ ] Base Speed (80-150)
        [ ] Skills -> Qtd enorme
            [ ] Extra Turn
            [ ] Extended (0-2)
            [ ] Rate (0-90)(%5)
            [ ] Turn Meter Fill (5-100)(5%)
            [ ] Countdown (0-7)
        [x] Preset: inits + orders -> 2.304
            [x] None
            [x] Opener
            [x] Off
            [x] OpenerOff
            [x] First
            [x] Second
            [x] Third
            [x] Forth
            [x] Fifth

            inits:
                parâmetros = [1, 2, 3, 4, 5]
                lp = 4
                opções = {
                    0: Free
                    1: Opener
                    2: Off
                    3: OpenerOff
                }

                * Cada parâmetro pode ter apenas 1 opção.
                * Todos parâmetros podem ter a opção 0.
                * Pode existir apenas 1 parâmetro com a opção 1.
                * Pode existir apenas 1 parâmetro com a opção 3.
                * Os parâmetros 1 e 3 não podem coexistir.
                    
                par 1: opções: (0, 1, 2, 3)
                par 2: opções: (0, 1, 2, 3)
                par 3: opções: (0, 1, 2, 3)
                par 4: opções: (0, 1, 2, 3)
                par 5: opções: (0, 1, 2, 3)

            orders:
                parâmetros = [1, 2, 3, 4, 5]
                opções = [1, 2, 3, 4, 5]

                * Cada parâmetro pode ter apenas 1 opção.
                * Todas opções devem ser diferentes.

                par 1: opções: (1, 2, 3, 4, 5)
                par 2: opções: (1, 2, 3, 4, 5)
                par 3: opções: (1, 2, 3, 4, 5)
                par 4: opções: (1, 2, 3, 4, 5)
                par 5: opções: (1, 2, 3, 4, 5)

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
from itertools import combinations, permutations, product
import random
import time

# ----------------------------------------------------------------------------------------------------------- #

def myPrint_01(iterable, group_size=5):
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

# ----------------------------------------------------------------------------------------------------------- #
pfc = { # PARAMETERS FOR COMBINATION
    'skill': [
        {'type': int, 'range': (0, 5), 'increment': 1},             # Countdown
        {'type': int, 'range': (0, 1), 'increment': 1},             # Extra Turn
        {'type': int, 'range': (0, 1), 'increment': 1},             # Buff Extend
        {'type': int, 'range': (0, 3), 'increment': 1},             # Buff Turns
        {'type': float, 'range': (0.0, 0.3), 'increment': 0.15},    # Speed Rate
        {'type': float, 'range': (0.0, 1.0), 'increment': 0.05}     # Turn Meter Fill
    ],
    'a1': [
        {'type': int, 'range': (0, 0), 'increment': 1},             # Countdown
        {'type': int, 'range': (0, 0), 'increment': 1},             # Extra Turn
        {'type': int, 'range': (0, 0), 'increment': 1},             # Buff Extend
        {'type': int, 'range': (0, 0), 'increment': 1},             # Buff Turns
        {'type': float, 'range': (0.0, 0.0), 'increment': 0.15},    # Speed Rate
        {'type': float, 'range': (0.0, 1.0), 'increment': 0.05}     # Turn Meter Fill
    ],
    'a2': [
        {'type': int, 'range': (1, 5), 'increment': 1},             # Countdown
        {'type': int, 'range': (0, 1), 'increment': 1},             # Extra Turn
        {'type': int, 'range': (0, 1), 'increment': 1},             # Buff Extend
        {'type': int, 'range': (0, 3), 'increment': 1},             # Buff Turns
        {'type': float, 'range': (0.0, 0.3), 'increment': 0.15},    # Speed Rate
        {'type': float, 'range': (0.0, 1.0), 'increment': 0.05}     # Turn Meter Fill
    ],
    'preset': {
        'ps1': [
            {'type': int, 'range': (0, 1), 'increment': 1},
            {'type': int, 'range': (0, 3), 'increment': 1},
            {'type': int, 'range': (0, 3), 'increment': 1},
            {'type': int, 'range': (0, 3), 'increment': 1},
            {'type': int, 'range': (0, 3), 'increment': 1}
        ],
        'ps2': (1, 2, 3, 4, 5)
    }
}

# ============================================= [ Presets Random ] ============================================= #
def rcg(parameters): # RANDON COMBINATION GENERATOR
    result = []
    if isinstance(parameters, tuple):
        return tuple(random.sample(parameters, len(parameters)))

    if isinstance(parameters, list) and len(parameters) > 1:
        for param in parameters:
            param_type = param['type']
            range_values = param['range']
            increment = param['increment']

            # Calcula o número de valores possíveis
            num_values = int((range_values[1] - range_values[0]) / increment) + 1

            # Seleciona um índice aleatório
            random_index = random.randint(0, num_values - 1)

            # Calcula o valor correspondente ao índice
            random_value = range_values[0] + random_index * increment

            # Se o tipo do parâmetro for float, arredonda para duas casas decimais
            if param_type == float:
                random_value = round(random_value, 2)

            result.append(random_value)

        return tuple(result)

    return None

def isValidSkill(par): # SKILL VALIDATOR
    return par[3] == 0 and par[4] == 0.0 or par[3] != 0 and par[4] != 0.0

def isValidPreset(par1, par2): # PRESET VALIDATOR
    return not (
            1 in par1 and 3 in par1 or
            par1.count(1) > 1 or
            par1.count(3) > 1 or
            par1.count(2) + par1.count(3) == len(par1)
        ) and par2[0] == 1

def rvcg(par, isValid): # RANDON VALID COMBINATION GENERATOR
    if callable(isValid):
        if isValid.__name__ == 'isValidSkill':
            result = rcg(par)
            if isValid(result):
                return result

        if isValid.__name__ == 'isValidPreset':
            result = [
                rcg(par['ps1']),
                rcg(par['ps2'])
            ]
            if isValid(result[0], result[1]):
                result.append(process_preset(*result))
                return result

        return rvcg(par, isValid)
    else:
        print('Insira uma função no parâmetro "isValid"')
    return None

def rvcg_skl_ps(): # RANDON VALID COMBINATION GENERATOR: SKILLS AND PRESET
    # Deve gerar:
    #   [ ] 1 Skill A1
    #   [ ] 4 Skill A2
    #   [ ] 1 Preset
    #   * Não pode gerar skills iguais.
    pass

# ============================================= [ Presets DataBase ] ============================================= #
def generate_combinations(parameters):
    values = []
    if isinstance(parameters, tuple):
        return list(permutations(parameters))
    
    if isinstance(parameters, list) and len(parameters) > 1:
        for param in parameters:
            param_type = param['type']
            range_values = param['range']
            increment = param['increment']

            if param_type == int:
                values.append(np.arange(range_values[0], range_values[1] + 1, increment).tolist())
            elif param_type == float:
                values.append(np.round(np.arange(range_values[0], range_values[1] + increment, increment), 2).tolist())
        return list(product(*values))

    return None

def initial_part_filter(combinations):
    """
    Filtra combinações com base nas regras fornecidas.
    """
    filtered = []
    length = len(combinations[0])
    for combination in combinations:
        if 1 in combination and 3 in combination:
            continue
        if combination.count(1) > 1 or combination.count(3) > 1:
            continue
        if combination.count(2) + combination.count(3) == length:
            continue
        filtered.append(combination)
    return filtered

def process_preset(condition_list, value_list):
    """
    Processa as listas fornecidas e retorna uma lista contendo:
    - o último índice de `condition_list` onde o valor é 1 ou 3,
    - seguido pelos índices dos valores positivos no resultado da soma vetorial de `value_list` e `adjustments`.
    """
    # Inicialização de variáveis
    adjustments = []
    last_valid_index = None

    # Preenchimento de `adjustments` e determinação de `last_valid_index` em uma única iteração
    for index, value in enumerate(condition_list):
        if value == 1 or value == 3:
            last_valid_index = index
        if value in (2, 3):
            adjustments.append(-6)
        else:
            adjustments.append(0)

    # Soma de vetores usando numpy arrays
    result_list = np.array(value_list) + np.array(adjustments)

    # Ordenar índices com base nos valores de result_list
    sorted_indices = [i for i, value in sorted(enumerate(result_list), key=lambda x: x[1], reverse=True) if value > 0]

    # Criar a lista final `final_result`
    return tuple([last_valid_index] + sorted_indices)

def generate_presets(parameters):
    """
    Gera os presets combinando e processando dados de `parameters`.
    """
    inits_combinations = generate_combinations(parameters['preset']['ps1'])
    orders_combinations = generate_combinations(parameters['preset']['ps2'])
    filtered_inits = initial_part_filter(inits_combinations)
    filtered_orders = [c for c in orders_combinations if c[0] == 1]

    presets = set()
    for order in filtered_orders:
        for init in filtered_inits:
            presets.add(process_preset(init, order))
    
    return presets
# ============================================= [ Testes ] ============================================= #

def testPreset(validations):
    valid_presets = generate_presets(pfc)
    v = 0
    while v < validations:
        ps = rvcg(pfc['preset'], isValidPreset)
        if ps[2] not in valid_presets:
            print("Preset Inválido:", ps)
        v+=1
        if v == validations:
            print("Todos Presets gerados são válidos!")

def testSkill(validations):
    valid_skills = [
        s for s in generate_combinations(pfc['skill']) 
        if not(s[3] != 0 and s[4] == 0.0 or s[3] == 0 and s[4] != 0.0)
    ]
    a1s = [a for a in valid_skills if a[0] == 0 and a[1] == 0 and a[2] == 0]
    a2s = [a for a in valid_skills if a[0] != 0]

    v = 0
    v1 = True
    v2 = True
    while v < validations:
        skill_a1 = rvcg(pfc['a1'], isValidSkill)
        skill_a2 = rvcg(pfc['a2'], isValidSkill)

        if skill_a1 not in a1s:
            v1 = False
            print("Skill A1 Inválida:", skill_a1)

        if skill_a2 not in a2s:
            v2 = False
            print("Skill A2 Inválida:", skill_a2)

        v+=1

        if v == validations:
            if v1:
                print("Todas Skills A1 geradas são válidas!")
            if v2:
                print("Todas Skills A2 geradas são válidas!")

preset = rvcg(pfc['preset'], isValidPreset)
skills = {
    'a1': rvcg(pfc['a1'], isValidSkill),
    'a2': rvcg(pfc['a2'], isValidSkill),
    'a3': rvcg(pfc['a2'], isValidSkill),
    'a4': rvcg(pfc['a2'], isValidSkill),
    'a5': rvcg(pfc['a2'], isValidSkill),
}
