import numpy as np
from itertools import permutations, product
import subprocess
import random

# ================================================================================================================ #
#                                                    Parameters
def pfc(): # PARAMETERS FOR COMBINATION
    return {
        'skills': [
            {'type': int, 'range': (0, 5), 'increment': 1},             # Countdown
            {'type': int, 'range': (0, 1), 'increment': 1},             # Extra Turn
            {'type': int, 'range': (0, 1), 'increment': 1},             # Buff Extend
            {'type': int, 'range': (0, 3), 'increment': 1},             # Buff Turns
            {'type': float, 'range': (0.0, 0.3), 'increment': 0.15},    # Speed Rate
            {'type': float, 'range': (0.0, 1.0), 'increment': 0.05}     # Turn Meter Fill
        ],
        'skill': {
            'a1': [
                {'type': int, 'range': (0, 0), 'increment': 1},             # Countdown
                {'type': int, 'range': (0, 0), 'increment': 1},             # Extra Turn
                {'type': int, 'range': (0, 0), 'increment': 1},             # Buff Extend
                {'type': int, 'range': (0, 0), 'increment': 1},             # Buff Turns
                {'type': float, 'range': (0.0, 0.0), 'increment': 0.15},    # Speed Rate
                {'type': float, 'range': (0.0, 0.1), 'increment': 0.05}     # Turn Meter Fill
            ],
            'a2': [
                {'type': int, 'range': (1, 7), 'increment': 1},             # Countdown
                {'type': int, 'range': (0, 1), 'increment': 1},             # Extra Turn
                {'type': int, 'range': (0, 1), 'increment': 1},             # Buff Extend
                {'type': int, 'range': (0, 3), 'increment': 1},             # Buff Turns
                {'type': float, 'range': (0.0, 0.3), 'increment': 0.15},    # Speed Rate
                {'type': float, 'range': (0.0, 1.0), 'increment': 0.05}     # Turn Meter Fill
            ]
        },
        'preset': {
            'ps1': [
                {'type': int, 'range': (0, 1), 'increment': 1},             # Free or Opener
                {'type': int, 'range': (0, 3), 'increment': 1},             # Free or Opener or Block or OpenerBlock
                {'type': int, 'range': (0, 3), 'increment': 1},             # Free or Opener or Block or OpenerBlock
                {'type': int, 'range': (0, 3), 'increment': 1},             # Free or Opener or Block or OpenerBlock
                {'type': int, 'range': (0, 3), 'increment': 1}              # Free or Opener or Block or OpenerBlock
            ],
            'ps2': (1, 2, 3, 4, 5)
        }
    }

# ================================================================================================================ #
#                                                    Random Skills
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

def rvcg(parameters=pfc()):  # SKILL PRESET GENERATOR
    def isValidSkill(par):  # SKILL VALIDATOR
        return (par[3] == 0 and par[4] == 0.0) or (par[3] != 0 and par[4] != 0.0)

    def isValidPreset(par1, par2):  # PRESET VALIDATOR
        return not (
                (1 in par1 and 3 in par1) or
                (par1.count(1) > 1) or
                (par1.count(3) > 1) or
                (par1.count(2) + par1.count(3) == len(par1))
            ) and (par2[0] == 1)
    
    # Criando 5 skills, sendo 1 a1 e 4 a2
    guide = ['a1', 'a2', 'a2', 'a2', 'a2']
    skills = set()
    
    for g in guide:
        skill = rcg(parameters['skill'][g])  # Gerando uma skill aleatória
        while not isValidSkill(skill) or skill in skills:
            skill = rcg(parameters['skill'][g])
        skills.add(skill)

    skills = list(skills)
    
    # Criando as duas partes do preset
    preset1 = rcg(parameters['preset']['ps1'])
    preset2 = rcg(parameters['preset']['ps2'])
    
    while not isValidPreset(preset1, preset2):
        preset1 = rcg(parameters['preset']['ps1'])
        preset2 = rcg(parameters['preset']['ps2'])

    preset = [preset1, preset2, process_preset(preset1, preset2)]
    skills.sort()
    
    return {'preset': preset, 'skills': skills}

# ================================================================================================================ #
#                                                    DataBase Skills
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
    inits_combinations = generate_combinations(parameters['preset']['preset']['ps1'])
    orders_combinations = generate_combinations(parameters['preset']['ps2'])
    filtered_inits = initial_part_filter(inits_combinations)
    filtered_orders = [c for c in orders_combinations if c[0] == 1]

    presets = set()
    for order in filtered_orders:
        for init in filtered_inits:
            presets.add(process_preset(init, order))
    
    return presets
# ================================================================================================================ #
#                                                    Área de Testes
def clear_console():
    subprocess.run(['cls'], shell=True) 

def myPrint_02(d):
    # Função auxiliar para converter o dicionário para o formato desejado
    def dict_to_json_str(d, indent=4):
        json_str = "{\n"
        for i, (key, value) in enumerate(d.items()):
            json_str += f'{" " * indent}{repr(key)}: [\n'
            for item in value:
                json_str += f'{" " * (indent * 2)}{item},\n'
            json_str = json_str.rstrip(',\n') + "\n"
            json_str += f'{" " * indent}],\n'
        json_str = json_str.rstrip(',\n') + "\n"
        json_str += "}"
        return json_str

    print(dict_to_json_str(d))

def gen_test(validations=1000):
    clear_console()
    parameters = pfc()
    skills_values = rvcg()
    v = 1
    z = 0
    while v <= validations:
        print(f"Combinação aleatória nº {v:05d}:")
        myPrint_02(skills_values)
        skills_values = rvcg()
        v+=1
        if z == 1:
            while True:
                user_input = input('Precione Enter para continuar')  # Aguarda o pressionamento de Enter
                clear_console()
                z=0
                # Verifica se o usuário pressionou Enter (entrada vazia)
                if user_input == "":
                    break
                # Aqui você pode adicionar a lógica que deseja executar dentro do loop
        else:
            z+=1

if __name__ == '__main__':
    gen_test(100)