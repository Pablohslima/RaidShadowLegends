import random

def rcg(parameters, quantity=1):
    """
    Gera combinações únicas de valores aleatórios a partir de uma tupla ou lista de parâmetros.

    Parameters:
    - parameters: Uma tupla de valores ou uma lista de dicionários que definem intervalos e incrementos.
    - quantity: Número de combinações únicas a serem geradas. O valor padrão é 1.

    Returns:
    - Uma lista de combinações únicas, ordenadas em ordem crescente.
    """
    
    # Caso os parâmetros sejam uma tupla
    if isinstance(parameters, tuple):
        # Verifica se a quantidade solicitada excede o número de permutações únicas possíveis
        if quantity > len(parameters):
            raise ValueError("Quantity exceeds the number of unique permutations available.")
        
        result = set()  # Usado para armazenar combinações únicas
        while len(result) < quantity:
            _res = tuple(random.sample(parameters, len(parameters)))  # Gera uma permutação aleatória dos elementos da tupla
            result.add(_res)  # Adiciona a permutação ao conjunto (evita duplicatas automaticamente)
        return sorted(result)  # Retorna as combinações únicas em ordem crescente

    # Caso os parâmetros sejam uma lista de dicionários
    if isinstance(parameters, list) and len(parameters) > 1:
        possible_values = []  # Lista para armazenar os possíveis valores para cada parâmetro
        
        for param in parameters:
            param_type = param['type']  # Tipo do parâmetro (int ou float)
            range_values = param['range']  # Intervalo de valores (lista com início e fim)
            increment = param['increment']  # Incremento entre os valores

            if param_type == int:
                # Gera uma lista de valores inteiros no intervalo especificado
                values = list(range(range_values[0], range_values[1] + 1, increment))
            elif param_type == float:
                # Gera uma lista de valores de ponto flutuante no intervalo especificado
                values = [round(value, 2) for value in frange(range_values[0], range_values[1], increment)]
            possible_values.append(values)  # Adiciona a lista de valores possíveis à lista principal

        result = set()  # Usado para armazenar combinações únicas
        while len(result) < quantity:
            # Gera uma combinação aleatória de valores possíveis para cada parâmetro
            _res = tuple(random.choice(values) for values in possible_values)
            result.add(_res)  # Adiciona a combinação ao conjunto (evita duplicatas automaticamente)
        return sorted(result)  # Retorna as combinações únicas em ordem crescente

    return None  # Retorna None se os parâmetros não forem válidos

def frange(start, stop, step):
    """
    Gera uma sequência de valores de ponto flutuante no intervalo especificado.

    Parameters:
    - start: Valor inicial.
    - stop: Valor final.
    - step: Incremento entre os valores.

    Yields:
    - Próximo valor na sequência.
    """
    while start < stop:
        yield start
        start += step
