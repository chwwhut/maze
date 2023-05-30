import csv
import numpy as np

"""
（1）迷宫：用Graph来表示，Graph以邻接表的形式储存。

（2）顶点：每个顶点以键值对的形式存在邻接表中，邻接表的键是顶点坐标（行，列）。
        值是保存该顶点信息的子字典，这个子字典需要保存的信息有：该顶点的值value（字符串形式）、该顶点的相邻顶点的坐标neighbors（列表形式）。

"""


def add_vertex(adj_list, value, loc):
    # 如果该点不在邻接表中，就加进去
    if loc not in adj_list:
        new_vertex = {'value': value, 'neighbors': []}
        # 如果它上面/左边有点，就把两点互相加到对方的neighbors列表里
        if (loc[0] - 1, loc[1]) in adj_list:
            adj_list[(loc[0] - 1, loc[1])]['neighbors'].append(loc)
            new_vertex['neighbors'].append((loc[0] - 1, loc[1]))
        if (loc[0], loc[1] - 1) in adj_list:
            adj_list[(loc[0], loc[1] - 1)]['neighbors'].append(loc)
            new_vertex['neighbors'].append((loc[0], loc[1] - 1))
        adj_list[loc] = new_vertex
    return adj_list


if __name__ == '__main__':
    with open('out.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = []
        for row in reader:
            data.append(row)

    maze = np.array(data)
    depth, breadth = maze.shape

    graph = {}

    for row in range(depth):
        for col in range(breadth):
            graph = add_vertex(graph, value=maze[row][col], loc=(row, col))

    print(graph)
