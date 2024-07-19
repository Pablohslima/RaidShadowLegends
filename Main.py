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
    [ ] Criar Skill genérica.
        [x] Criar DabaBase com todas combinações utilizadas nas Skills genéricas.
    [ ] Criar Preset.
        [ ] Criar DataBase com todas combinações utilizadas nos Presets.

3. [ ] Criar uma função capaz de definir se uma partida cumpre ou não a ocurrence definida.


* criar recurso que aplique esses recursos na rede neural
* em cada turno da rede neural ela pode executar tais acoes:
1. ver o resultado dos proximo turno(-0.5)
2. Reiniciar a corrida porem alterando os valores que inseriu. Futurmente alterando tambem os presets.(-1.0)
* -1.0 e -0.5 sao subtraidos da pontuacao dela.
* cada simulacao inicia com 10 pontos.
* em cada turno, satisfazendo a "meta" ela recebe +1.0
* em cada grupo de teste, aqueles com mais pontos serao replicados, os outros excluidos.
* talvez sejs necesserio outra ia pra dar suporte a isso.
# ============================= [ Informações ] ============================= #
# Turn Meter Max: 100
# Turn Meter Fill Rate: 0.07
# Turn Meter to Turn: 100/0.07 == 1428.57143
# Tick = Vel/TMT, exemplo: Vel == 190 Tick = 190/1428.57143 == 0.132299

# ============================== [ Entradas ] ============================== #
    [ ] Herois
        [ ] Base Speed (80-150)
        [ ] Skills (3) -> 4788
            [ ] Extended
            [ ] Rate (0-90)(%5)
            [ ] Turn Meter Fill (5-100)(5%) 
            [ ] Countdown (1-5)
        [ ] Preset: inits + orders
            [ ] None
            [ ] Opener
            [ ] Off
            [ ] OpenerOff
            [ ] First
            [ ] Second
            [ ] Third
            [ ] Forth
            [ ] Fifth

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

            presets:
                inits: (0, 2, 2, 3)
                orders: (1, 2, 3, 4, 5)






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


parCombination = {
    'skill': [
        {'type': int, 'range': (0, 2), 'increment': 1},             # Extend
        {'type': int, 'range': (0, 3), 'increment': 1},             # Turns
        {'type': int, 'range': (0, 5), 'increment': 1},             # Countdown
        {'type': float, 'range': (0.0, 0.9), 'increment': 0.05},    # Rate
        {'type': float, 'range': (0.0, 1.0), 'increment': 0.05}     # Fill
    ],
    'preset_init': [
        {'type': int, 'range': (0, 3), 'increment': 1},
        {'type': int, 'range': (0, 3), 'increment': 1},
        {'type': int, 'range': (0, 3), 'increment': 1},
        {'type': int, 'range': (0, 3), 'increment': 1},
        {'type': int, 'range': (0, 3), 'increment': 1}
    ],
    'preset_orders': (1, 2, 3, 4, 5)
}

def generate_presets():
    presets = []
    inits = []
    orders = []

    initsCombinations = generate_combinations(parCombination['preset_init'])
    ordersCombinations = generate_combinations(parCombination['preset_orders'])

    length = len(initsCombinations[0])

    for c in ordersCombinations:
        if c[0] != 1:
            continue
        orders.append(c)

    for c in initsCombinations:
        if c[0] in [2, 3]:
            continue
        if 1 in c and 3 in c:
            continue
        if c.count(1) > 1 or c.count(3) > 1:
            continue
        if c.count(2) + c.count(3) == length:
            continue
        inits.append(c)  # Adicionar como tupla para garantir unicidade

    for i in inits:
        preset = []
        for idx, par in enumerate(i):
            if par == 2:
                preset.append(0) # Block
        presets.append(preset)

    return inits

valid_presets = generate_presets()
valid_skills = generate_combinations(parCombination['skill'])
print(len(valid_presets))
myPrint_01(valid_presets, 5)