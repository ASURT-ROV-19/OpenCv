import numpy as np
import cv2
import argparse as m
from matplotlib import pyplot as plt

img = cv2.imread('cobalt-blue-daltile-tile-trim-dm141-261p2-64_1000.jpg')

hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

lower_blue=np.array([110,50,50])
upper_blue=np.array([130,255,255])

mask=cv2.inRange(hsv , lower_blue ,upper_blue)

res= cv2.bitwise_and(img,img,mask=mask)
#cv2.imshow('img',res)

#find end and start point
gray = cv2.cvtColor(res,cv2.COLOR_RGB2GRAY)

corners = cv2.goodFeaturesToTrack(gray,4,0.01,10)
corners = np.int0(corners)

for i in corners:
	x,y = i.ravel()
	cv2.circle(img,(x,y),3,(0,255,0),-1)

x1_blue,y1_blue= corners[0].ravel()
x2_blue,y2_blue= corners[1].ravel()
x3_blue,y3_blue= corners[2].ravel()
x4_blue,y4_blue= corners[3].ravel()

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

print line1
print line2
#print line3

if line1 < line2:
    lin_ref=line1
    pix_lin=line2
else :
    lin_ref=line2
    pix_lin=line1

len_of_line = (pix_lin * 1.9)/lin_ref

print (len_of_line)

len_of_line=str(len_of_line)
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img,len_of_line + 'cm',(10,200),font,2 ,(0,0,0),5)

cv2.imshow('img',img)

cv2.waitKey(0)
cv2.destroyAllWindows()