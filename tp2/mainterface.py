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
        # Calcula o caminho máximo a partir do vértice src utilizando uma variação do algoritmo de Dijkstra,
        # adaptada para encontrar o caminho de maior peso em vez do menor.

        dist = [-1e7] * self.V  # Inicializa todas as distâncias com um valor muito baixo (representando "infinito negativo").
        dist[src] = 0  # Define a distância do vértice de origem (src) para ele mesmo como 0.
        priority_queue = [(-0, src)]  # Fila de prioridade (min-heap) inicializada com a origem, usando distâncias negativas para maximizar.

        while priority_queue:
            current_dist, u = heapq.heappop(priority_queue)  # Remove o vértice com a maior distância (negativa) da fila de prioridade.
            current_dist = -current_dist  # Reverte o valor para obter a distância positiva correta.

            # Itera sobre todos os vizinhos do vértice u.
            for v, weight in self.graph[u]:
                # Se a distância até o vizinho v pelo vértice u for maior que a distância atual de v, atualiza-a.
                if dist[v] < dist[u] + weight:
                    dist[v] = dist[u] + weight  # Atualiza a distância de v com o novo caminho mais longo.
                    heapq.heappush(priority_queue, (-dist[v], v))  # Adiciona o vizinho v à fila com a nova distância negativa.

        return dist  # Retorna a lista de distâncias máximas de src para todos os vértices.


    def find_critical_path(self, dist):
        # Encontra o caminho crítico (caminho com maior duração total)
        # e o tempo máximo total de execução.

        # O caminho crítico começa do vértice com a maior distância acumulada.
        max_dist = max(dist)  # A maior distância é o tempo total máximo do caminho crítico.
        end_vertex = dist.index(max_dist)  # O vértice final do caminho crítico é aquele que atinge essa maior distância.

        # Inicia o processo de retroceder a partir do vértice final para encontrar o caminho completo.
        path = []  # Lista para armazenar os vértices que compõem o caminho crítico.
        current = end_vertex  # Começa do vértice final.
        
        # Retrocede pelos predecessores para reconstruir o caminho crítico.
        while current != -1:
            path.append(current)  # Adiciona o vértice atual ao caminho.
            found_predecessor = False  # Flag para verificar se encontramos o predecessor do vértice atual.
            
            # Itera sobre todos os vértices para encontrar o predecessor do vértice atual no caminho crítico.
            for v in range(self.V):
                for neighbor, weight in self.graph[v]:
                    # Verifica se a distância do vértice atual é igual à distância do predecessor mais o peso da aresta.
                    if neighbor == current and dist[current] == dist[v] + weight:
                        current = v  # Atualiza o vértice atual para o predecessor.
                        found_predecessor = True  # Marca que o predecessor foi encontrado.
                        break
                if found_predecessor:  # Sai do loop se o predecessor foi encontrado.
                    break
            
            if not found_predecessor:  # Se não houver mais predecessores, termina a reconstrução do caminho.
                break

        # O caminho foi construído do final para o início, então precisamos invertê-lo.
        path.reverse()  # Inverte a ordem para que o caminho comece no vértice inicial.
        
        # Retorna o caminho crítico e o tempo máximo (duração total do caminho).
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
