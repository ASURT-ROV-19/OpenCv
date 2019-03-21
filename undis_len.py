import numpy as np
import cv2
import argparse as m
from matplotlib import pyplot as plt
assert cv2.__version__[0] == '3', 'The fisheye module requires opencv version >= 3.0.0'
import os
import glob
import sys

DIM=(1920, 1080)
K=np.array([[1064.2342194939133, 0.0, 946.0467209407223], [0.0, 1062.0198205825952, 547.8331285822028], [0.0, 0.0, 1.0]])
D=np.array([[-0.10394777181581624], [-0.11445704940233585], [0.4632800102831019], [-0.45774793646474315]])


def edge_detect(frame):
  frame = cv2.Canny(frame, 100, 100)
  blur5 = cv2.GaussianBlur(frame,(5,5),0)
  blur3 = cv2.GaussianBlur(frame,(1,1),0)
  return blur5-blur3

img = cv2.imread('piic24.png')
####################################undistort################################
h,w = img.shape[:2]
map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
img=undistorted_img
###################################undistory##################################
#cv2.imshow('img',img)
width = img.shape[0]
height = img.shape[1]
boo=0

hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

lower_blue=np.array([110,50,50])
upper_blue=np.array([130,255,255])

mask=cv2.inRange(hsv , lower_blue ,upper_blue)

res1= cv2.bitwise_and(img,img,mask=mask)
#res =np.sum(res[0:height,0:width])
res =edge_detect(res1)

_,cnts_t,h  = cv2.findContours(res, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts_t = sorted(cnts_t, key = cv2.contourArea, reverse = True)[:2]
#cv2.imshow('img',res1)

cv2.drawContours(img, cnts_t, 0, (255,255,255), 3)
#cv2.imshow('img',img)

#Gets the length of biggest contor
peri = cv2.arcLength(cnts_t[0], True)
#Approximates the Contor we have to one with less vertices
approx = cv2.approxPolyDP(cnts_t[0], 0.02 * peri, True)
#same thing
#check the documentation:
#https://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html
vertices = cv2.convexHull(approx, clockwise=False)


for corner in vertices:
    x,y=corner[0].ravel()
    cv2.circle(img,(x,y),12,(0,0,255),-1)
    boo=boo+1
    if boo==1:
        x1_blue=x
        y1_blue=y
    elif boo==2:
        x2_blue=x
        y2_blue=y
    elif boo==3:
        x3_blue=x
        y3_blue=y
    elif boo==4:
        x4_blue=x
        y4_blue=y

        

#cv2.imshow('img',img)

####################################################################333
#find end and start point
gray = cv2.cvtColor(res1,cv2.COLOR_RGB2GRAY)


# x1_blue,y1_blue= corners[0].ravel()
# x2_blue,y2_blue= corners[1].ravel()
# x3_blue,y3_blue= corners[2].ravel()
# x4_blue,y4_blue= corners[3].ravel()

print ("x1 :",x1_blue," , y1 :",y1_blue)
print ("x2 :",x2_blue," , y2 :",y2_blue)
print ("x3 :",x3_blue," , y3 :",y3_blue)
print ("x4 :",x4_blue," , y4 :",y4_blue)

#cv2.imshow('img',img)

############################################calculat lin#########################
#corner1-corner2 toooooo line1
if abs(x1_blue-x2_blue) > abs(y1_blue-y2_blue) :
	line1 = abs(x1_blue-x2_blue)
else :
	line1 = abs(y1_blue-y2_blue)

#corner4-corner2 tooooo line2
if abs(x4_blue-x2_blue) > abs(y4_blue-y2_blue) :
	line2 = abs(x4_blue-x2_blue)
else :
	line2 = abs(y4_blue-y2_blue)

#corner3-corner2 tooooo line3
if abs(x3_blue-x2_blue) > abs(y3_blue-y2_blue) :
	line3 = abs(x3_blue-x2_blue)
else :
	line3 = abs(y3_blue-y2_blue)



if abs(line1-line2) > abs(line1-line3):
    line2=line2
else:
    line2=line3

print (line1)
print (line2)
#print line3

if line1 < line2:
    lin_ref=line1
    pix_lin=line2
else :
    lin_ref=line2
    pix_lin=line1

#width of lenth 1.7cm -----> change to 1.8 or 1.9
len_of_line = (pix_lin * 1.7)/lin_ref
len_of_line=round(len_of_line, 1)

print (len_of_line)

len_of_line=str(len_of_line)
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img,len_of_line + 'cm',(100,200),font,3 ,(0,0,0),5)

cv2.imshow('img',img)

cv2.waitKey(0)
cv2.destroyAllWindows()
