import csv
import networkx as nx

# Função para ler o arquivo CSV e montar o grafo
def ler_arquivo_csv(nome_arquivo):
    grafo = nx.DiGraph()  # Grafo direcionado para representar dependências
    with open(nome_arquivo, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            codigo = row['Codigo'].strip()
            nome = row['Nome']
            duracao = int(row['Duracao'])
            dependencias = row['Dependencias'].split(';') if row['Dependencias'] else []

            # Adiciona a disciplina como um nó no grafo
            grafo.add_node(codigo, nome=nome, duracao=duracao)

            # Adiciona as dependências (arestas) ao grafo
            for dependencia in dependencias:
                if dependencia:  # Verifica se existe uma dependência
                    grafo.add_edge(dependencia, codigo, weight=duracao)
                    
    return grafo

# Função para encontrar o caminho crítico (usando o algoritmo de Dijkstra)
def encontrar_caminho_critico(grafo):
    # Encontra os nós iniciais (sem predecessores) e finais (sem sucessores)
    nos_iniciais = [n for n, d in grafo.in_degree() if d == 0]
    nos_finais = [n for n, d in grafo.out_degree() if d == 0]

    if not nos_iniciais or not nos_finais:
        raise ValueError("O grafo deve ter pelo menos um nó inicial e um nó final.")

    # Utiliza o primeiro nó inicial e final encontrados para simplificação
    no_inicial = nos_iniciais[0]
    no_final = nos_finais[0]

    # Calcula o caminho mais curto de 'no_inicial' a 'no_final' usando Dijkstra
    caminho_critico = nx.dijkstra_path(grafo, source=no_inicial, target=no_final, weight='weight')
    tempo_minimo = nx.dijkstra_path_length(grafo, source=no_inicial, target=no_final, weight='weight')

    return caminho_critico, tempo_minimo

# Função principal para interação com o usuário
def main():
    while True:
        arquivo = input("Informe o arquivo (0 para sair): ")
        if arquivo == '0':
            break

        try:
            print("\nProcessando ...")
            grafo = ler_arquivo_csv(arquivo)
            caminho_critico, tempo_minimo = encontrar_caminho_critico(grafo)

            print("\nCaminho Crítico:")
            for node in caminho_critico:
                print(f"- {grafo.nodes[node]['nome']}")
            print(f"\nTempo Mínimo: {tempo_minimo}\n")

        except FileNotFoundError:
            print(f"Arquivo {arquivo} não encontrado. Tente novamente.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()
