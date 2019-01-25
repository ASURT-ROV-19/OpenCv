import numpy as np
import cv2
import argparse as m
from matplotlib import pyplot as plt

img = cv2.imread('Tast1.png')

gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)


corners = cv2.goodFeaturesToTrack(gray,4,0.01,10)
corners = np.int0(corners)

for i in corners:
	x,y = i.ravel()
	cv2.circle(img,(x,y),3,(0,255,0),-1)

x4,y4= corners[0].ravel()
x3,y3= corners[1].ravel()
x2,y2= corners[2].ravel()
x1,y1= corners[3].ravel()

if abs(x2-x1) > abs(y2-y1) :
	res_30 = abs(x2-x1)
else :
	res_30 = abs(y2-y1)

#print res_30

#blue line
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

lower_blue=np.array([110,50,50])
upper_blue=np.array([130,255,255])

mask=cv2.inRange(hsv , lower_blue ,upper_blue)

res= cv2.bitwise_and(img,img,mask=mask)

#find end and start point
gray = cv2.cvtColor(res,cv2.COLOR_RGB2GRAY)


corners = cv2.goodFeaturesToTrack(gray,2,0.01,10)
corners = np.int0(corners)

for i in corners:
	x,y = i.ravel()
	cv2.circle(img,(x,y),3,255,-1)

x1_blue,y1_blue= corners[0].ravel()
x2_blue,y2_blue= corners[1].ravel()

if abs(x2_blue-x1_blue) > abs(y2_blue-y1_blue) :
	res_line = abs(x2_blue-x1_blue)
else :
	res_line = abs(y2_blue-y1_blue)

#----------------------------
len_of_line = (res_line * 30)/res_30

print len_of_line

len_of_line=str(len_of_line)
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img,len_of_line + 'cm',(10,200),font,4 ,(0,0,0),5)


cv2.imshow('img',img)

cv2.waitKey(0)
cv2.destroyAllWindows()  
