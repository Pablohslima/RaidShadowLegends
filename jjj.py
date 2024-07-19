class Node:
    def __init__(self, label, properties):
        """
        Inicializa um nó do grafo com um rótulo e um conjunto de propriedades.

        :param label: Rótulo do nó (identificador único).
        :param properties: Dicionário contendo propriedades do nó.
        """
        self.label = label
        self.properties = properties
        self.edges = []  # Lista para armazenar arestas conectadas a este nó.

    def add_edge(self, edge):
        """
        Adiciona uma aresta à lista de arestas do nó.

        :param edge: Objeto Edge que representa a aresta conectando este nó a outro.
        """
        self.edges.append(edge)

    def __repr__(self):
        """
        Representação textual do nó para facilitar a visualização.

        :return: String representando o nó.
        """
        return f"Node(label={self.label}, properties={self.properties})"


class Edge:
    def __init__(self, start_node, end_node, label):
        """
        Inicializa uma aresta entre dois nós.

        :param start_node: Nó de início da aresta.
        :param end_node: Nó de fim da aresta.
        :param label: Rótulo da aresta.
        """
        self.start_node = start_node
        self.end_node = end_node
        self.label = label

    def __repr__(self):
        """
        Representação textual da aresta para facilitar a visualização.

        :return: String representando a aresta.
        """
        return f"Edge(start={self.start_node.label}, end={self.end_node.label}, label={self.label})"


class Graph:
    def __init__(self):
        """
        Inicializa um grafo vazio com um dicionário para armazenar nós e índices para propriedades.
        """
        self.nodes = {}  # Dicionário para armazenar nós, chave é o rótulo do nó.
        self.indexes = {}  # Dicionário para armazenar índices para propriedades dos nós.

    def add_node(self, label, properties):
        """
        Adiciona um nó ao grafo e atualiza os índices para as propriedades desse nó.

        :param label: Rótulo do nó.
        :param properties: Dicionário de propriedades do nó.
        :return: O nó adicionado.
        """
        node = Node(label, properties)
        self.nodes[label] = node
        
        # Atualiza os índices para cada propriedade do nó.
        for key, value in properties.items():
            if key not in self.indexes:
                self.indexes[key] = {}  # Cria um novo índice para a propriedade se não existir.
            if value not in self.indexes[key]:
                self.indexes[key][value] = []  # Cria uma nova lista para o valor se não existir.
            self.indexes[key][value].append(node)  # Adiciona o nó à lista de valores no índice.

        return node

    def add_edge(self, start_label, end_label, label):
        """
        Adiciona uma aresta entre dois nós no grafo.

        :param start_label: Rótulo do nó de início.
        :param end_label: Rótulo do nó de fim.
        :param label: Rótulo da aresta.
        """
        start_node = self.nodes.get(start_label)
        end_node = self.nodes.get(end_label)
        if start_node and end_node:
            edge = Edge(start_node, end_node, label)
            start_node.add_edge(edge)
            end_node.add_edge(edge)

    def find_nodes_by_properties(self, **kwargs):
        """
        Encontra nós que correspondem às propriedades especificadas.

        :param kwargs: Propriedades e valores para filtrar os nós.
        :return: Lista de nós que correspondem às propriedades fornecidas.
        """
        results = None  # Inicializa a lista de resultados como None.

        # Itera sobre cada propriedade fornecida na consulta.
        for key, value in kwargs.items():
            if key in self.indexes and value in self.indexes[key]:
                if results is None:
                    results = set(self.indexes[key][value])  # Inicializa results com o conjunto de nós que possuem o valor para a propriedade.
                else:
                    results.intersection_update(self.indexes[key][value])  # Interseção dos conjuntos para encontrar nós que satisfazem todas as condições.
            else:
                return []  # Retorna uma lista vazia se não houver correspondência.

        return list(results)  # Retorna a lista de nós que atendem a todas as propriedades.

# Exemplo de uso
grafo = Graph()

# Adicionar nós ao grafo
grafo.add_node("Tuple1", {"index1": 1, "index2": 2, "index3": 2, "index4": 4, "index5": 5})
grafo.add_node("Tuple2", {"index1": 2, "index2": 2, "index3": 3, "index4": 2, "index5": 1})
grafo.add_node("Tuple3", {"index1": 5, "index2": 2, "index3": 2, "index4": 7, "index5": 2})
grafo.add_node("Tuple4", {"index1": 2, "index2": 3, "index3": 2, "index4": 4, "index5": 2})
grafo.add_node("Tuple5", {"index1": 2, "index2": 2, "index3": 6, "index4": 2, "index5": 2})

# Consultar nós onde index2 e index4 são iguais a 2
resultados = grafo.find_nodes_by_properties(index2=2, index4=2)
for resultado in resultados:
    print(resultado)
