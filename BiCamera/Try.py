import cv2
import numpy as np
import glob
import os
import pickle

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


print('正在计算')
mtx = dist = rvecs = tvecs = newcameramtx = roi = None  # 给这些变量设置默认值
if os.path.exists("calibration_data.pkl"):
    # 如果有，就直接读取
    with open("calibration_data.pkl", "rb") as file:
        calibration_data = pickle.load(file)
    mtx = calibration_data['mtx']
    dist = calibration_data['dist']
    rvecs = calibration_data['rvecs']
    tvecs = calibration_data['tvecs']
    newcameramtx = calibration_data['newcameramtx']
    roi = calibration_data['roi']
else:
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
            # 储存标定时的图像
            cv2.imwrite('findCorners' + str(i) + '.jpg', img)
            cv2.waitKey(200)
    cv2.destroyAllWindows()
    if gray is not None:  # 如果gray不为空
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, gray.shape[::-1], 1, gray.shape[::-1])
        # 储存标定结果
        calibration_data = {'mtx': mtx, 'dist': dist, 'rvecs': rvecs, 'tvecs': tvecs, 'newcameramtx': newcameramtx, 'roi': roi}
        with open("calibration_data.pkl", "wb") as file:
            pickle.dump(calibration_data, file)
    else:
        print("无法计算相机标定，因为没有有效的图像")

# 以下代码未修改



if newcameramtx is not None and roi is not None:  # 如果newcameramtx和roi不为空
    camera = cv2.VideoCapture(0) # 打开摄像头
    # 检测摄像头是否打开
    if camera.isOpened():
        print('摄像头已经打开')
    else:
        print('摄像头未打开')

    while True:    # 持续读取摄像头
        (grabbed, frame) = camera.read() # 读取摄像头
        h1, w1 = frame.shape[:2]# 获取摄像头的高和宽
        # 提升分辨率
        frame = cv2.resize(frame, (int(w1 * 1.5), int(h1 * 1.5)), interpolation=cv2.INTER_CUBIC) # 放大摄像头长宽
        # 放大图像，全屏显示
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame', 640*2, 480*2)


        dst = cv2.undistort(frame, mtx, dist, None, newcameramtx) # 去畸变
        x, y, w1, h1 = roi # 获取去畸变后的图像的有效区域
        dst = dst[y:y + h1, x:x + w1] # 去除黑边
        cv2.imshow('frame', dst)
        #按下按键保存图片，并且继续读取摄像头。注意，保存图片后按序号保存，不要覆盖
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite('calibresult' + str(i) + '.jpg', dst)
            print("保存" + str(i))
            i = i + 1
            continue
        # 按下按键退出程序
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # 对保存下来的图片的边缘进行高亮显示
        gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY) # 转换为灰度图
        edges = cv2.Canny(gray, 100, 256, apertureSize=3)
        # 全屏显示
        cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('edges', 640*2, 480*2)

        cv2.imshow('edges', edges)

    camera.release()
    cv2.destroyAllWindows()
else:
    print("无法打开相机，因为没有有效的图像")
