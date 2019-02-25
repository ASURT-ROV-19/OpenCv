
# coding: utf-8

# In[1]:

import math
import cv2
import imutils
import numpy as np

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
    blur3 = cv2.GaussianBlur(img,(3,3),0)
    DoGim = blur5 - blur3
    kernelClose = np.ones((3, 3),np.uint8)

    DoGim = cv2.morphologyEx(DoGim, cv2.MORPH_CLOSE, kernelClose)
    #DoGim = cv2.morphologyEx(DoGim, cv2.MORPH_OPEN, kernelClose)

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
    temp = closing[0:R,0:C]
    edges =DoG(temp)
    
    ratio = image.shape[0] / float(image.shape[0])
    mx = np.amax(edges)
    mn = np.amin(edges)
    img=image
    thresh_val = np.average(np.arange(mn, mx))
    _, thresh = cv2.threshold(edges, thresh_val , 255, cv2.THRESH_BINARY)
    cv2.imshow("edge", thresh)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    #cnts=sorted(cnts, key=cv2.contourArea, reverse=True)
    
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
                #circle = shapes_count_safety_check(circle)+
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
    
    
image=cv2.imread("hope.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
mx = np.amax(gray)
mn = np.amin(gray)
thresh_val = np.average(np.arange(mn, mx))
_, thresh = cv2.threshold(gray, mx-50, 255, cv2.THRESH_BINARY)
color = ""
detectShapes(thresh,image)
cv2.imshow('image', image)

#cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()
