import networkx as nx
import matplotlib.pyplot as plt
import csv
import heapq

class Graph:
    def __init__(self, vertices):
        self.V = vertices  # Número de vértices
        self.graph = {v: [] for v in range(vertices)}  # Grafo representado por uma lista de adjacências
        self.vertex_map = {}  # Mapeamento de códigos de vértices para seus nomes

    def add_edge(self, u, v, weight):
        # Adiciona uma aresta do vértice u ao vértice v com o peso especificado
        self.graph[u].append((v, weight))

    def add_vertex(self, code, name):
        # Adiciona um vértice com um código e um nome
        self.vertex_map[code] = name

    def dijkstra_max_path(self, src):
        # Calcula o caminho máximo a partir do vértice src usando uma abordagem semelhante ao algoritmo de Dijkstra
        dist = [-1e7] * self.V  # Inicializa distâncias como um valor muito baixo
        dist[src] = 0  # A distância do vértice de origem para ele mesmo é 0
        priority_queue = [(-0, src)]  # Fila de prioridade (usando valor negativo para maximizar)

        while priority_queue:
            current_dist, u = heapq.heappop(priority_queue)
            current_dist = -current_dist  # Reverte o valor negativo para obter a distância real

            for v, weight in self.graph[u]:
                # Atualiza a distância se um caminho maior for encontrado
                if dist[v] < dist[u] + weight:
                    dist[v] = dist[u] + weight
                    heapq.heappush(priority_queue, (-dist[v], v))

        return dist

    def find_critical_path(self, dist):
        # Encontra o caminho crítico e o tempo máximo total
        max_dist = max(dist)  # A maior distância é o tempo total máximo
        end_vertex = dist.index(max_dist)  # Vértice final do caminho crítico

        # Retroceder para encontrar o caminho crítico
        path = []
        current = end_vertex
        while current != -1:
            path.append(current)
            found_predecessor = False
            for v in range(self.V):
                for neighbor, weight in self.graph[v]:
                    if neighbor == current and dist[current] == dist[v] + weight:
                        current = v
                        found_predecessor = True
                        break
                if found_predecessor:
                    break
            if not found_predecessor:
                break

        path.reverse()  # Inverte o caminho para a ordem correta do início ao fim
        return path, max_dist

    def draw_graph(self, path):
        # Desenha o grafo e destaca o caminho crítico
        G = nx.DiGraph()

        for u in range(self.V):
            G.add_node(self.vertex_map[list(self.vertex_map.keys())[u]])  # Adiciona o nó independentemente de arestas
            for v, weight in self.graph[u]:
                G.add_edge(self.vertex_map[list(self.vertex_map.keys())[u]], self.vertex_map[list(self.vertex_map.keys())[v]], weight=weight)
                
        pos = nx.spring_layout(G)
        labels = nx.get_edge_attributes(G, 'weight')

        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight='bold', arrows=True)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        # Destaca o caminho crítico em vermelho
        path_edges = [(self.vertex_map[list(self.vertex_map.keys())[path[i]]], self.vertex_map[list(self.vertex_map.keys())[path[i+1]]]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2.5)

        plt.title('Grafo com Caminho Crítico Destacado')
        plt.show()

def load_csv(filename):
    # Carrega o grafo a partir de um arquivo CSV
    with open(filename, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        data = list(csv_reader)
        vertices = len(data)
        graph = Graph(vertices)

        code_to_index = {}  # Mapeia códigos de vértices para seus índices
        index = 0
        for row in data:
            code = row['Codigo']
            name = row['Nome']
            graph.add_vertex(code, name)
            code_to_index[code] = index
            index += 1

        for row in data:
            u = code_to_index[row['Codigo']]
            duration = int(row['Duracao'])
            dependencies = row['Dependencias'].split(';')

            for dep in dependencies:
                if dep:
                    v = code_to_index[dep]
                    graph.add_edge(v, u, duration)

        return graph

def main():
    while True:
        filename = input("Informe o arquivo (0 para sair): ")
        if filename == "0":
            break

        print("Processando ...")

        graph = load_csv(filename)

        # Identifica nós iniciais (sem predecessores)
        initial_nodes = [i for i in range(graph.V) if not any(i in neighbors for neighbors in graph.graph.values())]

        max_path = []
        max_time = 0

        for start_node in initial_nodes:
            dist = graph.dijkstra_max_path(start_node)
            path, time = graph.find_critical_path(dist)
            if time > max_time:
                max_time = time
                max_path = path

        print("Caminho Crítico:")
        for vertex in max_path:
            print(f"- {graph.vertex_map[list(graph.vertex_map.keys())[vertex]]}")

        print(f"Tempo Mínimo: {len(max_path)}")
        print("Vértices:", graph.vertex_map)
        print("Arestas:", graph.graph)


        # Desenha o grafo com o caminho crítico destacado
        graph.draw_graph(max_path)

if __name__ == "__main__":
    main()
