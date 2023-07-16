import cv2
import os

def edge_detection(filename, number):
    # 构造完整的文件名
    full_filename = f"{filename}{number}.png"

    # 检查文件是否存在
    if not os.path.exists(full_filename):
        print(f"文件 {full_filename} 不存在")
        return None

    # 读取图像
    img = cv2.imread(full_filename)

    # 转换为灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 执行边缘检测
    edges = cv2.Canny(gray, 75, 250)

    # 返回边缘检测后的图像
    return edges

# 读取所有图像，名字为Image1.png, Image2.png, ..., Image10.png
for i in range(1, 11):
    edges = edge_detection("Image", i)

    # 显示图像
    if edges is not None:
        cv2.imshow('Edges', edges)
        cv2.destroyAllWindows()

    # 保存图像
    cv2.imwrite(f"Image{i}_edges.png", edges)
