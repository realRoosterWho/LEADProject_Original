import numpy as np
import cv2
import glob

# 设置迭代终止条件
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# 设置 object points, 形式为 (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((9*6, 3), np.float32)  # 根据实际棋盘格大小进行修改
objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)

# 用arrays存储所有图片的object points 和 image points
objpoints = []  # 3D点的实际坐标
imgpoints = []  # 2D点在图像平面的坐标

# 用glob匹配文件夹中所有文件名含有“.jpg"的图片
images = glob.glob("*.jpg")  # 根据实际路径进行修改

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 查找棋盘格角点
    ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)
    # 如果找到了就添加 object points, image points
    if ret == True:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)
        # 对角点连接画线加以展示
        cv2.drawChessboardCorners(img, (9, 6), corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(500)
cv2.destroyAllWindows()

# 标定
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
print(mtx, dist)

# 其他代码...
# 对所有图片进行去畸变
images = glob.glob("/*.jpg")
for fname in images:
    prefix = fname.split('/')[1]
    img = cv2.imread(fname)
    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

    # 使用 cv.undistort()进行畸变校正
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    # 对图片有效区域进行剪裁
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]
    cv2.imwrite('/undistort/' + prefix, dst)

# 重投影误差计算
mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
    mean_error += error

print("total error: ", mean_error / len(objpoints))
