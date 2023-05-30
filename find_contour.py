import cv2 as cv


def find_contour(filename):
    original_image = cv.imread(filename)
    image = original_image.copy()
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)  # 获取灰度图
    blurred = cv.GaussianBlur(gray, (3, 3), 0)
    canny = cv.Canny(blurred, 120, 255, 1)  # 边缘检测

    # 在图像中寻找轮廓
    cnts = cv.findContours(canny.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # 获取每个轮廓的区域
    contour_sizes = [(cv.contourArea(contour), contour) for contour in cnts]

    # 寻找最大轮廓并且截取ROI区域
    if len(contour_sizes) > 0:
        largest_contour = max(contour_sizes, key=lambda x: x[0])[1]
        x, y, w, h = cv.boundingRect(largest_contour)
        cv.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
        ROI = original_image[y:y + h, x:x + w]
        cv.imshow("ROI", ROI)
    cv.imwrite('maze.bmp', ROI)  # 保存裁剪后的迷宫图片

    # cv.imshow("canny", canny)
    cv.imshow("original", image)
    cv.waitKey(0)


if __name__ == '__main__':
    find_contour('migong.bmp')