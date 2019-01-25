import cv2
assert cv2.__version__[0] == '3', 'The fisheye module requires opencv version >= 3.0.0'
import numpy as np
import os
import glob
import sys

DIM=(1920, 1080)
K=np.array([[1064.2342194939133, 0.0, 946.0467209407223], [0.0, 1062.0198205825952, 547.8331285822028], [0.0, 0.0, 1.0]])
D=np.array([[-0.10394777181581624], [-0.11445704940233585], [0.4632800102831019], [-0.45774793646474315]])


def undistort(img_path):

	img = cv2.imread(img_path)
	h,w = img.shape[:2]
	map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
	undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

	cv2.imshow("undistorted", undistorted_img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

if __name__ == '__main__':
    for p in sys.argv[1:]:
        undistort('WIN_20181204_10_14_46_Pro.jpg')
