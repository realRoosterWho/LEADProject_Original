# -*- coding: utf-8 -*-
import cv2
import time

AUTO = True  # 自动拍照，或手动按s键拍照
INTERVAL = 2  # 自动拍照间隔

# 创建左右两个窗口
cv2.namedWindow("left")
cv2.namedWindow("right")

# 打开摄像头
camera = cv2.VideoCapture(0)

# 设置分辨率 左右摄像机同一频率，同一设备ID；左右摄像机总分辨率1280x480；分割为两个640x480、640x480
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280*2)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480*2)

counter = 0
utc = time.time()
folder = ""  # 拍照文件目录
def shot(pos, frame):
    global counter
    path = folder + pos + "_" + str(counter) + ".jpg"

    cv2.imwrite(path, frame)
    print("snapshot saved into: " + path)

while True:
    ret, frame = camera.read()

    # 裁剪坐标为[y0:y1, x0:x1] HEIGHT*WIDTH
    left_frame = frame[0:(480*2), 0:(640*2)]
    right_frame = frame[0:(480*2), (640*2):(1280*2)]

    # 显示左右图像
    cv2.imshow("left", left_frame)
    cv2.imshow("right", right_frame)

    now = time.time()
    if AUTO and now - utc >= INTERVAL:
        shot("left", left_frame)
        shot("right", right_frame)
        counter += 1
        utc = now

    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    elif key == ord("s"):
        shot("left", left_frame)
        shot("right", right_frame)
        counter += 1

# 释放摄像头资源
camera.release()

# 关闭窗口
cv2.destroyWindow("left")
cv2.destroyWindow("right")

