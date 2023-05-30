import csv

with open('out.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    maze = []
    for row in reader:
        maze.append(row)


# 1可走, 0不可走
m, n = len(maze), len(maze[0])  # m * n 迷宫
start = (0, 1)  # 起点
end = (31, 29)  # 终点

""" DFS 深度优先搜索 """

# 记录每个单元格的访问情况，防止重复访问。
# visited[x][y] = 1 表示(x,y)位置已经访问过，visited初始全为False。
visited = [[False] * n for _ in range(m)]  # m * n 大小
path = []  # 用于临时记录当前走过的路径，全局变量，格式：[(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
result = []  # 用于记录所有可行的路径，全局变量


# 寻找所有路径的DFS
def dfs_all(maze, start, end, max_paths=1000):
    global visited, path, result  # 扩展全局变量作用域到此处（否则默认会当成局部变量）
    x, y = start  # 当前（递归到此处）的起点
    # （对于任何递归函数，在进行下一层递归操作前必定先判断是否能够继续递归。否则会出现无限递归的情况）
    # 先判断是否越界，然后判断是否可走，最后判断是否已经访问过
    if 0 <= x < m and 0 <= y < n and maze[x][y] == '1' and visited[x][y] is False:
        # 既然满足了上面的条件，那么就说明当前位置是可走的
        visited[x][y] = True  # ① 当前位置标记为走过
        path.append((x, y))  # ② 将当前位置加入到路径中
        if len(result) > max_paths:
            return 1
        if start == end:  # 如果当前位置(start)就是终点，那么成功找到了一条路径
            result.append(path.copy())  # 记录当前路径 (注意：这里必须是path.copy()，不能直接赋值！！！否则后面path.pop()会导致result也被pop())
        # 当前位置已走过，准备寻找新的位置
        # 分别试探当前位置上下左右四个方向的路径
        # 以下四行代码的顺序可以随意调换，该顺序会影响到探索策略，即先探索哪个方向的新位置。
        # 所以可能导致答案不同（但有答案就一定能找到）
        dfs_all(maze, (x + 1, y), end)  # 传递新的start进去，向下继续搜索
        dfs_all(maze, (x - 1, y), end)  # 传递新的start进去，向上继续搜索
        dfs_all(maze, (x, y + 1), end)  # 传递新的start进去，向右继续搜索
        dfs_all(maze, (x, y - 1), end)  # 传递新的start进去，向左继续搜索
        visited[x][y] = False  # 回溯，将当前位置重新标记为未访问
        path.pop()  # 回溯，将当前位置从路径中移除
        # 回溯代码前已经遍历了当前位置的所有上下左右方向，已无新路可走，那么当然要“走回头路”，撤销此步选择。


dfs_all(maze, start, end)
print('所有可行的路径：')
for i in result:
    print(i)