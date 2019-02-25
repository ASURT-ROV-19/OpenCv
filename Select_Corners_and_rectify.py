import cv2
from transform import four_point_transform
import numpy as np

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
counter=0
points=[]

def point_select(event, x, y, flags, param):
	# grab references to the global variables
	global refPt, counter , points

	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x, y)]
		points.append((x,y))

image = cv2.imread("pic3.jpg")
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", point_select)

while  True:
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("r"):
        image = clone.copy()
    if key == ord("c"):
        break

points=np.array(points)
warped = four_point_transform(image, points)
 
# show the original and warped images
cv2.imshow("Original", image)
cv2.imshow("Warped", warped)
cv2.imwrite("hope.png",warped)
cv2.waitKey(0)