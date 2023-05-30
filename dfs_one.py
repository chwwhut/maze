import csv
from matrix_to_graph import add_vertex


""" 
DFS 深度优先搜索 
只寻找一条路径的DFS
"""
# 记录每个单元格的访问情况，防止重复访问。
# visited[x][y] = 1 表示(x,y)位置已经访问过，visited初始全为False。
visited = [[False] * 32 for _ in range(32)]  # m * n 大小 简单直接赋值32
path = []  # 用于临时记录当前走过的路径，全局变量，格式：[(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
result = []  # 用于记录一条可行的路径，全局变量，格式和上面一样
flag = False  # 用于标记是否找到一条可行的路径，全局变量


def dfs(graph, start, end):
    global visited, path, result, flag  # 扩展全局变量作用域到此处（否则默认会当成局部变量）
    x, y = start  # 当前（递归到此处）的起点
    # （对于任何递归函数，在进行下一层递归操作前必定先判断是否能够继续递归。否则会出现无限递归的情况）
    # 先判断是否已找到一条可行的路径，再判断是否可走，最后判断是否已经访问过
    if not flag and graph[(x, y)]['value'] == '1' and visited[x][y] is False:
        # 既然满足了上面的条件，那么就说明当前位置是可走的
        visited[x][y] = True  # ① 当前位置标记为走过
        if start == end:  # 如果当前位置(start)就是终点，那么成功找到了一条路径
            # 由于此时path中还没有加入end，所以需要在此处加入end
            result = path.copy() + [end]  # 记录当前路径
            flag = True  # 找到一条可行的路径，将flag置为True
            return  # 结束递归（第一种情况）
        path.append((x, y))  # ② 将当前位置加入到路径中
        # 当前位置已走过，准备寻找新的位置
        # 分别试探当前位置邻边的路径
        for new_start in graph[(x, y)]['neighbors']:
            dfs(graph, new_start, end)
        path.pop()  # 回溯，将当前位置从路径中移除

        """ 
        回溯代码前已经遍历了当前位置的所有邻边，
        说明此处的上下左右都找过了，已无路可走，那么当然要“走回头路”，撤销此步选择。 
        """
    return result


if __name__ == '__main__':
    with open('out.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        maze = []
        for row in reader:
            maze.append(row)

    depth, breadth = len(maze), len(maze[0])

    graph = {}  # 以图来存储迷宫，顶点为每个格子，共1024个顶点，边为该顶点的相邻顶点的坐标neighbors（以列表形式存储）

    # 循环添加全部顶点
    for row in range(depth):
        for col in range(breadth):
            graph = add_vertex(graph, value=maze[row][col], loc=(row, col))

    print(graph)

    # 记录每个单元格的访问情况，防止重复访问。
    # visited[x][y] = 1 表示(x,y)位置已经访问过，visited初始全为False。

    # 1可走, 0不可走
    m, n = len(maze), len(maze[0])  # m * n 迷宫
    start = (0, 1)  # 起点
    end = (31, 29)  # 终点

    dfs(graph, start, end)  # DFS搜索
    if result:  # 如果有解
        print('此迷宫的一条可行路径为:', result)
    else:
        print('无路可走！')

    result_dfs = result
