#task0
#Графы
#циклические планарные неориентированный (без стрелочек)
#невзвешенный (не нагруженный, без меток)
#таблица смежности
#бритва акаме
#список ребер
#теория множеств - язык для записи математики
#U ()
#граф множество рёбер, ребро - множество из двух элементов, элемент - множество из 1 элемента
#G -граф
#V - ребро
#e - edges
#G=(V,E)
#упорядоченные - упорядоченная пара
#{} - неупорядоченное
#() / <> - упорядоченные
#V={'1','2','3','4'}
#v1 - элемент
#V={v1,v2,v3,v4}
#E={e1,e2,e3,e4}
#e1={v1,v2}
#{e1,e2,ei,em} ei Э(перевернуть горизонтально) E e1={Vi,Vk}
#S Э Vi
#Si={}
#нагрузим
#e1=(v1,v2,G)
#ei=(vi,vk,mi)
#K Э mi
#V:set[str]={'v1','v2','v3','v4'}
#E:set[tuple[str,str,float]]={('v1','v2',25),('v1','v3',13),(),()}
#v1,v2,25\n
#v1,v3,13\n
#концепция компьютера - машина тьюринга - лента знаков
#CSV на вход
#вернуть граф матрицы смежности
#main(v:str):list[list]


from typing import List, Dict, Tuple
import csv
import io

#Принимает вход как CSV (многострочная строка)
#Возвращает список пар (v1, v2)
def csv_input(input_str: str) -> List[Tuple[str, str]]:
    
    reader = csv.reader(io.StringIO(input_str.strip()))
    edges = []
    
    #Фильтрация пустых элементов и пробелов
    for row in reader:
        if not row:
            continue
        row = [c.strip() for c in row if c is not None and c.strip() != '']
        if not row:
            continue
        if row[0].startswith('#'):
            continue
        if len(row) < 2:
            continue
        v1, v2 = row[0], row[1]
        edges.append((v1, v2))
    return edges

#Строит невзвешенный неориентированный граф и возвращает (matrix, vertices),
#где vertices - список вершин в порядке первого появления
def build_graph_unweighted(edge_pairs: List[Tuple[str, str]]) -> Tuple[List[List[int]], List[str]]:
    order: List[str] = []
    index: Dict[str, int] = {}
    for v1, v2 in edge_pairs:
        for v in (v1, v2):
            if v not in index:
                index[v] = len(order)
                order.append(v)

    n = len(order)
    matrix: List[List[int]] = [[0 for _ in range(n)] for __ in range(n)]
    for v1, v2 in edge_pairs:
        i, j = index[v1], index[v2]
        matrix[i][j] = 1
        matrix[j][i] = 1

    return matrix, order

#main(v: str) -> (matrix, vertices)
#Принимает CSV (многострочная строка) или путь к файлу содержимого
#Возвращает матрицу смежности и список вершин в порядке первого появления
def main(v: str) -> Tuple[List[List[int]], List[str]]:
    edge_pairs = csv_input(v)
    matrix, vertices = build_graph_unweighted(edge_pairs)
    return matrix, vertices

if __name__ == "__main__":
    with open('task2.csv', 'r', encoding='utf-8') as file:
        s = file.read()
    matrix, vertices = main(s)
    print("Вершины:", vertices)
    print("Матрица смежности:")
    for row in matrix:
        print(row)
