import numpy as np
from itertools import permutations, product
from collections import deque
from printers import format_as_json
import subprocess
import random

# ================================================================================================================ #
#                                                    Parameters
def param_config(): # PARAMETERS FOR COMBINATION
    return {
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
                {'type': int, 'range': (0, 1), 'increment': 1}, # Free or Opener
                {'type': int, 'range': (0, 3), 'increment': 1}, # Free or Opener or Block or OpenerBlock
                {'type': int, 'range': (0, 3), 'increment': 1}, # Free or Opener or Block or OpenerBlock
                {'type': int, 'range': (0, 3), 'increment': 1}, # Free or Opener or Block or OpenerBlock
                {'type': int, 'range': (0, 3), 'increment': 1}  # Free or Opener or Block or OpenerBlock
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

def rvcg(parameters=param_config()):  # SKILL PRESET GENERATOR
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

def rvcg_test(zf=0, validations=1000):
    clear_console()
    parameters = param_config()
    skills_values = rvcg()
    v = 1
    z = 0
    flag = True
    while v <= validations and flag:
        print(f"Combinação aleatória nº {v:05d}:")
        skill_print(skills_values)
        skills_values = rvcg()
        v+=1
        if z == zf:
            while flag:
                user_input = input('Pressione Enter para continuar')  # Aguarda o pressionamento de Enter
                clear_console()
                z=0
                # Verifica se o usuário pressionou Enter (entrada vazia)
                if user_input == "":
                    break
                if user_input.upper() in {'QUIT', 'EXIT', 'OFF', 'Q'}:
                    flag = False
                    break
        else:
            z+=1
    return None

class RandomGenerator:
    def __init__(self, config=None):
        self._config = config if isinstance(config, dict) else param_config()
        self._current = ()
        self._saved = deque(maxlen=10)

    def __getitem__(self, key):
        return self._config[key]
    
    def __setitem__(self, key, value):
        self._config[key] = value

    @property
    def config(self):
        return self._config

    @property
    def current(self):
        return self._current

    def new(self, quantity=1):
        try:
            if isinstance(quantity, (int, float)) and quantity >= 1:
                self._current = [rvcg(self.config) for _ in range(int(quantity))]
                if quantity == 1:
                    return self._current[0]  # Retorna o único conjunto de parâmetros diretamente
                else:
                    return self._current  # Retorna a lista de conjuntos de parâmetros
            else:
                raise ValueError("Insira um valor válido para quantity (inteiro maior ou igual a 1).")
        except ValueError as e:
            print(e)
            return None
    
    def save(self):
        for index in self.current:
            self._saved.append(index)
        return tuple(self._saved)
    def test(self, max_combinations=100, pause_interval=1):
        """
        Gera e exibe uma série de combinações aleatórias até o limite definido,
        pausando para entrada do usuário em intervalos definidos.

        Parameters:
        - max_combinations (int): O número máximo de combinações a serem geradas.
        - pause_interval (int): O número de combinações entre pausas.
        """
        clear_console()
        count = 1  # Contador de combinações
        pause_counter = 0  # Contador para pausas
        continue_flag = True  # Flag para controlar a continuidade do loop

        while count <= max_combinations and continue_flag:
            print(f"Combinação aleatória nº {count:05d}:")
            print(
                format_as_json(self.new())
            )
            count += 1

            if pause_counter == pause_interval:
                while continue_flag:
                    user_input = input('Pressione ENTER para continuar ou digite "QUIT" para sair: ').strip()
                    clear_console()
                    pause_counter = 0
                    
                    if user_input == "":
                        break
                    if user_input.upper() in {'QUIT', 'EXIT', 'OFF', 'Q'}:
                        continue_flag = False
                        break
            else:
                pause_counter += 1

        return None

if __name__ == '__main__':
    rg = RandomGenerator()
    print(rg.config)