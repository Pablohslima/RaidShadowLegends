exercicios = [
    ("2x - 3 > 5", "x > 4"),
    ("4x + 1 <= 9", "x <= 2"),
    ("5 - x < 7", "x > -2"),
    ("3x + 2 >= 11", "x >= 3"),
    ("-2x + 4 < 8", "x > -2"),
    ("6x - 5 >= 13", "x >= 3"),
    ("7x + 4 <= 18", "x <= 2"),
    ("9 - 3x > 0", "x < 3"),
    ("4x - 7 <= 9", "x <= 4"),
    ("-5x + 6 >= 1", "x <= 1"),
    ("2x + 3 > 7", "x > 2"),
    ("3 - 2x < 1", "x > 1"),
    ("5x - 2 <= 8", "x <= 2"),
    ("6 - 3x >= 3", "x <= 1"),
    ("4x + 5 < 13", "x < 2"),
    ("7x - 4 > 10", "x > 2"),
    ("9x + 1 <= 19", "x <= 2"),
    ("-3x + 2 >= -7", "x <= 3"),
    ("8x - 5 < 3", "x < 1"),
    ("6 + 2x > 10", "x > 2"),
    ("5x + 4 <= 14", "x <= 2"),
    ("-2x + 3 < 5", "x > -1"),
    ("3x - 6 >= 9", "x >= 5"),
    ("4x + 7 < 19", "x < 3"),
    ("-5x + 8 <= 3", "x >= 1"),
    ("2x - 1 > 3", "x > 2"),
    ("7 - 3x < 4", "x > 1"),
    ("6x + 2 <= 20", "x <= 3"),
    ("8 - 4x >= 0", "x <= 2"),
    ("3x + 5 < 14", "x < 3")
]

for e in exercicios:
    inequacao = e[0]
    resposta = e[1]
    
    # Calcula o tamanho necessário para preencher até 15 caracteres
    padding_length = 30 - len("|" + inequacao + ":" + " " + resposta + "|")
    
    # Preenche com hífens à direita para completar 15 caracteres
    string_formatada = "|" + inequacao + ":" + " " * padding_length + resposta + "|"
    
    print(string_formatada)