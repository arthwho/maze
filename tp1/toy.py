from collections import deque
import time

def solve_maze_bfs(maze):
    """Função que resolve o labirinto com busca em largura (BFS) e retorna o caminho percorrido e o tamanho do caminho."""
    R, C = len(maze), len(maze[0])

    start = (0, 0)
    for r in range(R):
        for c in range(C):
            if maze[r][c] == 'S':
                start = (r, c)
                break
        else:
            continue
        break
    else:
        return None, None

    queue = deque()
    queue.appendleft((start[0], start[1], 0, [start[0] * C + start[1]]))
    directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    visited = [[False] * C for _ in range(R)]

    while len(queue) != 0:
        coord = queue.pop()
        visited[coord[0]][coord[1]] = True

        if maze[coord[0]][coord[1]] == "E":
            return coord[2], [[i // C, i % C] for i in coord[3]]

        for dir in directions:
            nr, nc = coord[0] + dir[0], coord[1] + dir[1]
            if (nr < 0 or nr >= R or nc < 0 or nc >= C or maze[nr][nc] == "#" or visited[nr][nc]): continue
            queue.appendleft((nr, nc, coord[2] + 1, coord[3] + [nr * C + nc]))

    return None, None

def solve_maze_dfs(maze):
    """Função que resolve o labirinto com busca em profundidade (DFS) e retorna o caminho percorrido e o tamanho do caminho."""
    R, C = len(maze), len(maze[0])

    start = (0, 0)
    for r in range(R):
        for c in range(C):
            if maze[r][c] == 'S':
                start = (r, c)
                break
        else:
            continue
        break
    else:
        return None, None

    stack = [(start[0], start[1], 0, [start[0] * C + start[1]])]
    directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    visited = [[False] * C for _ in range(R)]

    while len(stack) != 0:
        coord = stack.pop()
        visited[coord[0]][coord[1]] = True

        if maze[coord[0]][coord[1]] == "E":
            return coord[2], [[i // C, i % C] for i in coord[3]]

        for dir in directions:
            nr, nc = coord[0] + dir[0], coord[1] + dir[1]
            if (nr < 0 or nr >= R or nc < 0 or nc >= C or maze[nr][nc] == "#" or visited[nr][nc]): continue
            stack.append((nr, nc, coord[2] + 1, coord[3] + [nr * C + nc]))

    return None, None

def main():
    while True:
        print("3 - maze/maze3.txt", end="      ")
        print("10 - maze/maze10.txt", end="        ")
        print("20 - maze/maze20.txt")
        print("30 - maze/maze30.txt", end="        ")
        print("40 - maze/maze40.txt", end="        ")
        print("50 - maze/maze50.txt")
        print("0 - Sair")

        choice = input("Informe um arquivo para leitura: ")

        if choice == "0":
            print("Finalizando o programa.")
            break
        elif choice == "3":
            file_name = "maze/maze3.txt"
        elif choice == "10":
            file_name = "maze/maze10.txt"
        elif choice == "20":
            file_name = "maze/maze20.txt"
        elif choice == "30":
            file_name = "maze/maze30.txt"
        elif choice == "40":
            file_name = "maze/maze40.txt"
        elif choice == "50":
            file_name = "maze/maze50.txt"
        else:
            print("Escolha inválida.")
            continue

        try:
            with open(file_name, encoding="utf-8") as f:
                maze = [list(line.strip("\n")) for line in f]

            # Busca em largura (BFS)
            start_time_bfs = time.time()
            path_len_bfs, path_items_bfs = solve_maze_bfs(maze)
            end_time_bfs = time.time()
            bfs_time = end_time_bfs - start_time_bfs

            # Busca em profundidade (DFS)
            start_time_dfs = time.time()
            path_len_dfs, path_items_dfs = solve_maze_dfs(maze)
            end_time_dfs = time.time()
            dfs_time = end_time_dfs - start_time_dfs

            # Resultados BFS
            print("\nBusca em Largura (BFS):")
            if path_len_bfs is not None:
                print("Tamanho do caminho:", path_len_bfs)
                print("Caminho realizado:", path_items_bfs)
                print(f"Tempo de execução: {bfs_time:.4f} segundos")
            else:
                print("Caminho não encontrado.")

            # Resultados DFS
            print("\nBusca em Profundidade (DFS):")
            if path_len_dfs is not None:
                print("Tamanho do caminho:", path_len_dfs)
                print("Caminho realizado:", path_items_dfs)
                print(f"Tempo de execução: {dfs_time:.4f} segundos")
            else:
                print("Caminho não encontrado.")

        except FileNotFoundError:
            print(f"Erro: {file_name} não encontrado.")
        except Exception as e:
            print(f"Um erro ocorreu: {e}")

        continue_choice = input("\nLer mais arquivos? (y/n): ").strip().lower()
        if continue_choice != "y":
            print("Finalizando o programa.")
            break

if __name__ == "__main__":
    main()
