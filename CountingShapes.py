
# coding: utf-8

# In[1]:

import math
import cv2
import imutils
import numpy as np

q=0

#old params#
DIM=(640, 480)
K=np.array([[491.30957471682893, 0.0, 307.4549785636325], [0.0, 474.1090441470422, 253.85204028435578], [0.0, 0.0, 1.0]])
D=np.array([[-0.09562009684692586], [-0.3023857004224222], [1.5141194223421497], [-2.155421082692752]])

#get new from bishr.



def undistort(img_path):    
    
    h,w = img_path.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img_path, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    #cv2.imshow("im",undistorted_img)
    return undistorted_img
	
    

# In[2]:

def shapes_count_safety_check(x):
    if (x)<=6:
        x+=1
        return x
    else:
        return x

unknowns=[]

def rectangle_or_line(approx,img):
    vertices = cv2.convexHull(approx, clockwise=True)
    #########################
    x1,y1=vertices[0].ravel()
    x2,y2=vertices[1].ravel()
    x3,y3=vertices[-1].ravel()
    #########################
    #cv2.circle(img, (x1,y1), 10, (255,255,255), thickness=1)
    #cv2.circle(img, (x2,y2), 10, (0,0,0), thickness=1)
    #cv2.circle(img, (x3,y3), 10, (0,0,255), thickness=1)
    #########################
    side3_1=math.hypot(x1-x3,y1-y3)
    side3_2=math.hypot(x2-x1,y2-y1)
    ratio= side3_1 / (side3_2 * 1.0)
    #cv2.line(img,(x1,y1),(x3,y3),(130,130,130),4)
    #cv2.line(img,(x2,y2),(x1,y1),(130,130,130),4)
    print(ratio)
    if (ratio >= 4) or  (ratio <= 0.4) :
        print("line")
        print(ratio)
        return("line")
    elif (ratio>= 0.5 ) and (ratio <= 1.3):
        print(ratio)
        
        return("rectangle")

rectangle_parameters=[]

def detect(c,img,cnts,thresh):
    global rectangle_parameters
    approx = cv2.approxPolyDP(c, 0.04 * cv2.arcLength(c, True), True)
    shape = ''
    if len(approx) == 3:
        shape = "triangle"
        # print(shape)

    elif len(approx) == 4:
        shape=rectangle_or_line(approx,img)
        
        
        
    else:
        global unknowns
        unknowns.append(c)
        shape="circle"
        

    return shape


# In[3]:

q=0

def DoG(img):
    global q
    blur5 = cv2.GaussianBlur(img,(5,5),0)
    blur3 = cv2.GaussianBlur(img,(1,1),0)
    DoGim = blur5 - blur3
    kernelClose = np.ones((3, 3),np.uint8)

    DoGim = cv2.morphologyEx(DoGim, cv2.MORPH_CLOSE, kernelClose)

    #DoGim = cv2.medianBlur(DoGim,5)
    
    return DoGim


# In[4]:


def detectShapes(mask,image):
    X = 20
    Y = 20
    line = 0
    rectangle = 0
    circle = 0
    triangle = 0
    kernelopen = np.ones((5, 5), np.uint8)
    kernelClose = np.ones((3, 3),np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelopen)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernelClose)
    R=closing.shape[0]
    C=closing.shape[1]
    temp = closing[0:R-150,0:C-150]
    edges =DoG(temp)
    
    ratio = image.shape[0] / float(image.shape[0])
    
    
#     lines = cv2.HoughLinesP(edges,1,np.pi/180,50,minLineLength=20,maxLineGap=60)

#     if (lines is None):
#         return
#     N = lines.shape[0]
#     for i in range(N):
#         x1 = lines[i][0][0]
#         y1 = lines[i][0][1]
#         x2 = lines[i][0][2]
#         y2 = lines[i][0][3]
#         cv2.line(edges, (x1, y1), (x2, y2), (255, 0, 0), 2)

    mx = np.amax(edges)
    mn = np.amin(edges)
    img=image
    thresh_val = np.average(np.arange(mn, mx))
    _, thresh = cv2.threshold(edges, thresh_val , 255, cv2.THRESH_BINARY)
    cv2.imshow("edge", thresh)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(img, cnts, 0, (0,255,0), 3)
    
    #cv2.imshow("test",img)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    #cv2.drawContours(img, cnts, -1, (0,255,0), 3)
    ###########################Edits to think about######################################
    if (len(cnts)>=15):
        #this means that extra shapes are detected
        #print("There is more contours detected than needed")
        #we will then take only the largest contours
        cnts=sorted(cnts, key=cv2.contourArea, reverse=True)
    ########################################################################################
#     for c in cnts:
#         M=cv2.moments(c)
# #         cX = int((M["m10"]/M["m00"])*ratio)
# #         cY = int((M["m01"]/M["m00"])*ratio)
        
#         shape = detect(c)
#         c = c.astype("float")
#         c *= ratio
#         c = c.astype("int")

#         cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
# #         cv2.putText(image, color +" " + shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 0), 2)


    for c in cnts:
        if cv2.arcLength(c, True)>50:       #this is the condition to eliminate small curves 
            shape = detect(c,img,cnts,thresh)
            if (shape == "triangle"):
                triangle += 1
                cv2.drawContours(img, c, -1, (0,255,0), 3)

                #triangle = shapes_count_safety_check(triangle)
            elif (shape == "circle"):
                circle += 1
                cv2.drawContours(img, c, -1, (189,255,30), 3)
                #circle = shapes_count_safety_check(circle)
            elif (shape == "rectangle"):
                rectangle += 1
                cv2.drawContours(img, c, -1, (0,0,0), 3)

                #rectangle = shapes_count_safety_check(rectangle)
            elif (shape == "line"):
               line += 1
               cv2.drawContours(img, c, -1, (0,0,255), 3)

               #line = shapes_count_safety_check(line)

    cv2.putText(image, str(line), (X, Y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.line(image, (X + 30, Y - 2), (X + 70, Y - 2), (0, 0, 255), 4)

    cv2.putText(image, str(circle), (X, Y + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.circle(image, (X + 40, Y + 35), 15, (0, 0, 255), -1)

    cv2.putText(image, str(rectangle), (X, Y + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.rectangle(image, (X + 25, Y + 60), (X + 55, Y + 90), (0, 0, 255), -1)

    pt1 = (X + 40, Y + 100)
    pt2 = (X + 20, Y + 130)
    pt3 = (X + 60, Y + 130)
    triangle_cnt = np.array([pt1, pt2, pt3])
    cv2.drawContours(image, [triangle_cnt], 0, (0, 0, 255), -1)
    cv2.putText(image, str(triangle) + " ", (X, Y + 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    #cv2.imwrite("pic.png",image)
    

# In[ ]:

i=True
cap = cv2.VideoCapture(0)
while (i):
    for i in range(15):
        cap.grab()
    (grabbed, image) = cap.read()
   # image=undistort(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    mx = np.amax(gray)
    mn = np.amin(gray)

    thresh_val = np.average(np.arange(mn, mx))
    _, thresh = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
    #thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
    color = ""
    detectShapes(thresh,image)
    cv2.imshow('image', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

#cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()
