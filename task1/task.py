from typing import List, Tuple
import csv

def main(s: str, e: str) -> Tuple[
    List[List[bool]],
    List[List[bool]], 
    List[List[bool]],
    List[List[bool]],
    List[List[bool]]
]:
    # Считывание данных из CSV-файла
    edges = []
    nodes = set()
    
    # Если s - это путь к файлу, читаем из файла
    try:
        with open(s, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                if len(row) >= 2:
                    source = row[0].strip()
                    target = row[1].strip()
                    edges.append((source, target))
                    nodes.add(source)
                    nodes.add(target)
    except FileNotFoundError:
        # Если файл не найден, пытаемся обработать s как CSV-строку
        for line in s.strip().split('\n'):
            if line.strip():
                parts = line.split(',')
                if len(parts) >= 2:
                    source = parts[0].strip()
                    target = parts[1].strip()
                    edges.append((source, target))
                    nodes.add(source)
                    nodes.add(target)
    
    # Добавляем корневой узел, если его нет в данных
    if e not in nodes:
        nodes.add(e)
    
    # Создаем упорядоченный список всех узлов
    nodes = sorted(nodes)
    n = len(nodes)
    node_to_index = {node: idx for idx, node in enumerate(nodes)}
    
    # Инициализация матриц
    r1 = [[False] * n for _ in range(n)]  # прямое управление
    r2 = [[False] * n for _ in range(n)]  # прямое подчинение  
    r3 = [[False] * n for _ in range(n)]  # опосредованное управление
    r4 = [[False] * n for _ in range(n)]  # опосредованное подчинение
    r5 = [[False] * n for _ in range(n)]  # соподчинение
    
    # Построение графа и матрицы r1 (прямое управление)
    graph = {node: [] for node in nodes}
    for source, target in edges:
        i, j = node_to_index[source], node_to_index[target]
        r1[i][j] = True
        graph[source].append(target)
    
    # Матрица r2 - прямое подчинение (транспонирование r1)
    for i in range(n):
        for j in range(n):
            r2[i][j] = r1[j][i]
    
    # Построение матрицы r3 (опосредованное управление) через DFS
    def dfs(start: int, current: int, visited: List[bool]):
        for neighbor in graph[nodes[current]]:
            neighbor_idx = node_to_index[neighbor]
            if not visited[neighbor_idx]:
                visited[neighbor_idx] = True
                r3[start][neighbor_idx] = True
                dfs(start, neighbor_idx, visited)
    
    for i in range(n):
        visited = [False] * n
        dfs(i, i, visited)
    
    # Матрица r4 - опосредованное подчинение (транспонирование r3)
    for i in range(n):
        for j in range(n):
            r4[i][j] = r3[j][i]
    
    # Построение матрицы r5 (соподчинение)
    # Находим всех детей для каждого родителя
    parent_children = {}
    for source, target in edges:
        if source not in parent_children:
            parent_children[source] = []
        parent_children[source].append(target)
    
    # Для каждого родителя связываем всех его детей между собой
    for children in parent_children.values():
        if len(children) > 1:
            for i in range(len(children)):
                for j in range(i + 1, len(children)):
                    idx1 = node_to_index[children[i]]
                    idx2 = node_to_index[children[j]]
                    r5[idx1][idx2] = True
                    r5[idx2][idx1] = True
    
    return r1, r2, r3, r4, r5

# Пример использования с вашим файлом task2.csv
if __name__ == "__main__":
    # Чтение из файла task2.csv
    filename = "task2.csv"
    root = "1"  # корневой узел
    
    result = main(filename, root)
    
    # Вывод результатов
    relations = ["r1 - прямое управление", 
                 "r2 - прямое подчинение", 
                 "r3 - опосредованное управление", 
                 "r4 - опосредованное подчинение", 
                 "r5 - соподчинение"]
    
    # Получаем список узлов из файла
    nodes = set()
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                if len(row) >= 2:
                    nodes.add(row[0].strip())
                    nodes.add(row[1].strip())
    except FileNotFoundError:
        # Если файл не найден, используем пример данных
        nodes = {'1', '2', '3', '4', '5'}
    
    if root not in nodes:
        nodes.add(root)
    
    nodes = sorted(nodes)
    
    print("Узлы:", nodes)
    print("\n" + "="*50)
    
    for i, (name, matrix) in enumerate(zip(relations, result)):
        print(f"\n{name}:")
        print("   " + "  ".join(nodes))
        for j, row in enumerate(matrix):
            print(f"{nodes[j]}  " + "  ".join(str(int(x)) for x in row))

result = main("task2.csv", "1")
