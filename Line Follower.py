import cv2
import math
import numpy as np

Video = cv2.VideoCapture(0)
flag = 0
R1 = 0
R2 = 0
R3 = 0
R4 = 0
R5 = 0
R6 = 0
red = 49000
current_dir = 'right'
def change_dirr (dir,R1,R2,R3):
    if R2 >= red and R1 < red and R3 < red:
        return dir
    if dir == 'down' or dir == 'up':
        if R1 > red and R2 > red and R3 < red:
            return 'left'
        elif R1 < red and R2 > red and R3 > red:
            return 'right'

    elif dir == 'left' or dir == 'right':
        if R1 > red and R2 > red and R3 < red:
            return 'up'
        elif R1 < red and R2 > red and R3 > red:
            return 'down'
    return dir


while True:

    _, img = Video.read()
#    img = cv2.imread('s2.jpg',cv2.IMREAD_COLOR)
    # =======to draw the rectangles only=====
    imgVeritcal = img
    imgHorizontal = img
    # =======================================

    # detect red lines
    # =======================================
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # ============  Camera Laptop Helaly =============
    # min = np.array([0, 40, 40])
    # max = np.array([100, 150, 150])
    # ============  Camera Tape3ia =============
    # min = np.array([0, 100, 50])
    # max = np.array([20, 240, 240])
    min = np.array([150, 40, 40])
    max = np.array([180, 255, 255])

    mask = cv2.inRange(hsv, min, max)
    height, width = img.shape[:2]
    res1 = cv2.bitwise_and(img, img, mask=mask)
    res2 = res1

    kernal = np.ones((5, 5), np.uint8)
    res1 = cv2.morphologyEx(res1, cv2.MORPH_CLOSE, kernal)
    # ===============Vertical Reigons======================
    roi1 = res1[0:height, 0:width // 3]
    roi2 = res1[0:height, width // 3: 2 * width // 3]
    roi3 = res1[0:height, 2 * width // 3:width]

    roi1 = cv2.cvtColor(roi1, cv2.COLOR_HSV2BGR)
    roi2 = cv2.cvtColor(roi2, cv2.COLOR_HSV2BGR)
    roi3 = cv2.cvtColor(roi3, cv2.COLOR_HSV2BGR)
    # =====================================================

    # ===============Horizontal Reigons======================
    roi4 = res1[0:height // 3, 0:width]
    roi5 = res1[height // 3 :2 * height // 3, 0: width]
    roi6 = res1[2 * height // 3:height,0:width]

    roi4 = cv2.cvtColor(roi4, cv2.COLOR_HSV2BGR)
    roi5 = cv2.cvtColor(roi5, cv2.COLOR_HSV2BGR)
    roi6 = cv2.cvtColor(roi6, cv2.COLOR_HSV2BGR)
    # =====================================================

    # Get the dimensions of the Reigon!
    roi1_h, roi1_w = roi1.shape[:2]
    roi4_h, roi4_w = roi4.shape[:2]
    w = cv2.waitKey(3) & 0xFF

    if w == ord('a'):
        flag = 1
        for i in range(roi1_h - 1):
            for j in range(roi1_w - 1):
                k = roi1[i, j]
                z = roi2[i, j]
                q = roi3[i, j]
                R1 += k[2] + k[1] + k[0]
                R2 += z[2] + z[1] + z[0]
                R3 += q[2] + q[1] + q[0]

        current_dir = change_dirr(current_dir,R1,R2,R3)
        print(current_dir)
        # print (R1)
        # print (R2)
        # print (R3)

    if w == ord('h'):
        flag = 2
        for i in range(roi4_h - 1):
            for j in range(roi4_w - 1):
                k1 = roi4[i, j]
                z1 = roi5[i, j]
                q1 = roi6[i, j]
                R4 += k1[2] + k1[1] + k1[0]
                R5+= z1[2] + z1[1] + z1[0]
                R6 += q1[2] + q1[1] + q1[0]

        current_dir = change_dirr(current_dir,R4,R5,R6)
        print(current_dir)
        # print (R4)
        # print (R5)
        # print (R6)

    if (flag == 0) | (flag == 1):
        cv2.rectangle(res1, (0, 0), (width // 3, height), (0, 255, 0), 1)
        cv2.rectangle(res1, (width // 3, 0), (2 * width // 3, height), (0, 255, 0), 1)
        cv2.rectangle(res1, (2 * width // 3, 0), (width, height), (0, 255, 0), 1)
        cv2.imshow("img", res1)

    if (flag == 2):
        cv2.rectangle(res2, (0, 0), (width, height // 3), (0, 255, 0), 1)
        cv2.rectangle(res2, (0, height // 3), (width, 2 * height // 3), (0, 255, 0), 1)
        cv2.rectangle(res2, (0, 2 * height // 3), (width, height), (0, 255, 0), 1)
        cv2.imshow("img", res2)

    R1 = 0
    R2 = 0
    R3 = 0
    R4 = 0
    R5 = 0
    R6 = 0

    # cv2.imshow("H1", roi4)
    # cv2.imshow("H2", roi5)
    # cv2.imshow("H3", roi6)


    if (w == ord('q')):
        break

cv2.destroyAllWindows()



