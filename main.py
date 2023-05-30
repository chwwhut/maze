import csv

import cv2

from bfs import bfs
from dfs_one import dfs
from find_contour import find_contour
from img_to_matrix import *
from matrix_to_graph import add_vertex

# 设置 numpy 的打印选项,将 numpy 数组的打印阈值设置为无穷大,这意味着数组的所有元素都将被打印.
np.set_printoptions(threshold=np.inf)

"""
用Python的OpenCV库来读取一张图片，然后对图片进行灰度化、高斯模糊、边缘检测等操作。
接着，使用cv.findContours()函数寻找图像中的轮廓，并获取每个轮廓的区域。
最后，找到最大轮廓并且截取ROI区域，保存裁剪后的迷宫图片。
处理图片生成32*32矩阵（0表示黑色，1表示白色）:
"""
# 将图片进行裁剪得到迷宫图片
find_contour('migong.bmp')

# 将迷宫图片转换为矩阵并输出到csv文件
data = imageToMatrix('maze.bmp')
print(data)

# np.savetxt('out.csv', data, delimiter=",")   # 此处生成的csv文件在excel中做过改动，原来存储类型为float 现存储类型为string ：'0'，'1'

# 将矩阵转换为图片
new_im = matrixToImage(data)
plt.imshow(data, cmap=plt.cm.gray, interpolation="nearest")
new_im.show()

"""
对矩阵进行处理，用合适的数据结构描述顶点与边，利用算法自动生成数据结构；
说明思路:

（1）迷宫：用Graph来表示，Graph以邻接表的形式储存。

（2）顶点：每个顶点以键值对的形式存在邻接表中，邻接表的键是顶点坐标（行，列）。
        值是保存该顶点信息的子字典，这个子字典需要保存的信息有：该顶点的值value（字符串形式）、该顶点的相邻顶点的坐标neighbors（列表形式）。
        eg: {
              (0, 0): {'value': '0', 'neighbors': [(0, 1), (1, 0)]},
              (0, 1): {'value': '1', 'neighbors': [(0, 0), (0, 2), (1, 1)]},
              ...
              (31, 30): {'value': '1', 'neighbors': [(30, 30), (31, 29), (31, 31)]}, 
              (31, 31): {'value': '0', 'neighbors': [(30, 31), (31, 30)]}
            }
"""
# 读取保存到csv文件的矩阵，以二维列表maze存储
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

"""
搜索起点到终点的道路；
道路条数很多，下面展示用DFS搜索到的一条路径
在dfs_all中展示搜索全部路径代码，可更改最大的搜索路径数
"""

# 记录每个单元格的访问情况，防止重复访问。
# visited[x][y] = 1 表示(x,y)位置已经访问过，visited初始全为False。

# 1可走, 0不可走
start = (0, 1)  # 起点
end = (31, 29)  # 终点

result = dfs(graph, start, end)  # DFS搜索
if result:  # 如果有解
    print('此迷宫的一条可行路径为:', result)
else:
    print('无路可走！')

result_dfs = result

"""
BFS获得最短路径；
"""
result = bfs(graph, start, end)
if result:
    print('最短路径：')
    print(result)  # 输出最短路径
    print('最短路径长度:', len(result)-1)  # 输出最短路径长度，减1是因为两个点之间的距离是两个点之间的边数
else:
    print('没有找到路径！')

result_bfs = result

"""
图形化显示迷宫及路径；
"""

# 读取迷宫图片并转化为灰度图像
img = cv2.imread('maze.bmp', 0)

# 将灰度图像进行二值化处理
threshold = 127
_, img_gray = cv2.threshold(img, threshold, 1, cv2.THRESH_BINARY)

# 调整二值化后的矩阵形状为 32x32，并将像素值转换为整型
img_resized = cv2.resize(img_gray, (32, 32), interpolation=cv2.INTER_AREA)
maze_matrix = img_resized.astype(int)
# print(maze_matrix)  # 打印二维数组，0表示障碍物，1表示通道

# 显示DFS搜索到的其中一条路径
for i in range(len(result_dfs)-1):
    x1, y1 = result_dfs[i]
    x2, y2 = result_dfs[i+1]
    plt.plot([y1, y2], [x1, x2], '-b', linewidth=5)

# 显示迷宫图像
plt.imshow(maze_matrix, cmap='gray')
plt.xticks([]), plt.yticks([])
#
plt.legend(["DFS"], loc='upper right')
plt.show()


# 显示BFS搜索到的最短路径
for i in range(len(result_bfs)-1):
    x1, y1 = result_bfs[i]
    x2, y2 = result_bfs[i+1]
    plt.plot([y1, y2], [x1, x2], '-r', linewidth=5)

# 显示迷宫图像
plt.imshow(maze_matrix, cmap='gray')
plt.xticks([]), plt.yticks([])
#
plt.legend(["BFS"], loc='upper right')
plt.show()