import PIL.Image as Image
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import cv2 as cv



#利用摄像头对迷宫图片拍照
def get_photo():
    cap = cv.VideoCapture(0) #开启摄像头
    while True:
        f, frame = cap.read() #将摄像头中的一帧图片数据保存
        cv.imwrite('maze.jpg', frame) #将图片保存为本地文件
        cv.imshow('maze', frame)
        cv.waitKey(25)
        cv.destroyAllWindows()
        cap.release() #关闭摄像头
        break

#读图片
def read_photo():
    #img = cv.imread("./image/migong.bmp") # 直接图迷宫图片
    img = cv.imread("./maze.jpg")  # 读取利用摄像头拍得的迷宫图片
    cv.namedWindow('maze', cv.WINDOW_NORMAL)  # 自适应窗口
    cv.imshow('maze', img)
    cv.waitKey(0)
    cv.destroyAllWindows()

# 处理图片生成32*32的矩阵（0表示黑色 1表示白色）
# 将图片转换为矩阵
def imageToMatrix(filename):
    #读取图片
    img = Image.open(filename)

    #显示图片
    # img.show()
    img = img.resize((32, 32))
    width, height = img.size
    #灰度化
    img = img.convert("L")
    data = img.getdata()
    data = np.matrix(data, dtype="float")/255.0
    data = np.reshape(data, (height, width))

    m, n = img.size
    for i in range(n):
        for j in range(m):
            if data[i, j] > 0.5:
                data[i, j] = 1
            else:
                data[i, j] = 0
    return data

# 将矩阵转换为图片
def matrixToImage(data):
    data = data * 255.0
    new_im = Image.fromarray(data)
    return new_im


if __name__=='__main__':
    # get_photo()
    # read_photo()
    # 将图片转换为矩阵并输出到csv文件
    data = imageToMatrix('maze.bmp')
    print(data)
    np.savetxt('out.csv', data, delimiter=",")
    # 将矩阵转换为图片
    new_im = matrixToImage(data)
    plt.imshow(data, cmap=plt.cm.gray, interpolation="nearest")
    new_im.show()