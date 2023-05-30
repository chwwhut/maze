import csv
from queue import Queue


from matrix_to_graph import add_vertex

visited = [[False] * 32 for _ in range(32)]  # m * n 大小
result = []  # 用于记录一条最短的路径，全局变量，格式和上面一样
path = []  # 用于临时记录当前走过的路径，全局变量，格式：[(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]


def bfs(graph, start, end):
    global visited, path, result
    queue = Queue()  # 创建一个队列，用于广度遍历
    father = {}  # 用于记录每个单元格的上一步单元格
    x, y = start  # 起点，取出(x, y)方便后面使用
    queue.put(start)  # 将起点放入队列
    visited[x][y] = True  # 将起点标记为已访问
    father[(x, y)] = None  # 起点没有上一步，所以标记为None,
    while not queue.empty():  # 队列不为空时就循环
        cur = queue.get()  # 访问出队列中的第一个元素(同时具有读取和删除的功能)
        x, y = cur  # 解包出(x, y)方便后面使用
        visited[x][y] = True  # 将当前位置标记为已访问
        if cur == end:  # 如果当前位置是终点，就结束搜索
            # 根据father字典，从终点往回找，找到起点为止，就是一条最短路径
            while cur is not None:
                result.append(cur)
                cur = father[cur]
            result = result[::-1]  # 反转一下，从起点到终点
            return result  # 返回，结束搜索

        for next_pos in graph[cur]['neighbors']:  # 遍历当前位置的上下左右四个方向
            x_next, y_next = next_pos  # 解包出(x_next, y_next)方便后面使用
            # 判断是否是障碍物，是否已经访问过
            if graph[next_pos]['value'] == '1' and not visited[x_next][y_next]:
                queue.put(next_pos)  # 将下一个可行位置加入队列
                father[next_pos] = cur  # 将下一个可行位置的上一步单元格(下一个的上一个，就是当前单元格)记录下来


if __name__=='__main__':
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

    # print(graph)

    # 记录每个单元格的访问情况，防止重复访问。
    # visited[x][y] = 1 表示(x,y)位置已经访问过，visited初始全为False。

    m, n = len(maze), len(maze[0])  # m * n 迷宫
    start = (0, 1)  # 起点
    end = (31, 29)  # 终点

    visited = [[False] * n for _ in range(m)]  # m * n 大小
    result = []  # 用于记录一条最短的路径，全局变量，格式和上面一样
    path = []  # 用于临时记录当前走过的路径，全局变量，格式：[(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]

    bfs(graph, start, end)
    if result:
        print('最短路径：')
        print(result)  # 输出最短路径
        print('最短路径长度:', len(result) - 1)  # 输出最短路径长度，减1是因为两个点之间的距离是两个点之间的边数
    else:
        print('没有找到路径！')

