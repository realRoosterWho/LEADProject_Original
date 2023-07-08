import cv2
import numpy as np
import glob

# 找棋盘格角点
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)  # 阈值
w = 9  # 9个内角点
h = 6  # 6个内角点
objp = np.zeros((w * h, 3), np.float32)
objp[:, :2] = np.mgrid[0:w, 0:h].T.reshape(-1, 2)
objp = objp * 18.1  # 18.1 mm

objpoints = []  # 在世界坐标系中的三维点
imgpoints = []  # 在图像平面的二维点
images = glob.glob('./*.jpg')  # 拍摄的十几张棋盘图片所在目录

gray = None  # 在循环外部定义gray
i = 0
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (w, h), None)
    if ret == True:
        print("i:", i)
        i = i + 1
        cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        objpoints.append(objp)
        imgpoints.append(corners)
        cv2.drawChessboardCorners(img, (w, h), corners, ret)
        cv2.namedWindow('findCorners', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('findCorners', 640, 480)
        cv2.imshow('findCorners', img)
        cv2.waitKey(200)
cv2.destroyAllWindows()

print('正在计算')
mtx = dist = rvecs = tvecs = newcameramtx = roi = None  # 给这些变量设置默认值
if gray is not None:  # 如果gray不为空
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, gray.shape[::-1], 1, gray.shape[::-1])
else:
    print("无法计算相机标定，因为没有有效的图像")

if newcameramtx is not None and roi is not None:  # 如果newcameramtx和roi不为空
    camera = cv2.VideoCapture(0)
    while True:
        (grabbed, frame) = camera.read()
        h1, w1 = frame.shape[:2]
        dst = cv2.undistort(frame, mtx, dist, None, newcameramtx)
        x, y, w1, h1 = roi
        dst = dst[y:y + h1, x:x + w1]
        cv2.imshow('frame', dst)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # 按q保存一张图片
            cv2.imwrite("./frame.jpg", dst)
            break
    camera.release()
    cv2.destroyAllWindows()
else:
    print("无法打开相机，因为没有有效的图像")
