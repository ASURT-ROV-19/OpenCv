import math
import cv2
import imutils
import numpy as np


def detect(c,img,cnts,thresh):
    approx = cv2.approxPolyDP(c, 0.04 * cv2.arcLength(c, True), True)
    shape=''
    arr=''
    if len(approx) == 4:
        shape='rectangle'
        vertices = cv2.convexHull(approx, clockwise=True)
        #########################
        x1,y1=vertices[0].ravel()
        x2,y2=vertices[1].ravel()
        x3,y3=vertices[-1].ravel()
        x4,y4=vertices[2].ravel()
        #########################
        #print(x3,y3)
        cv2.circle(img, (x1,y1), 10, (255,255,255), thickness=1)
        cv2.circle(img, (x2,y2), 10, (0,0,0), thickness=1)
        cv2.circle(img, (x3,y3), 10, (0,0,255), thickness=1)
        cv2.circle(img, (x4,y4), 10, (255,0,0), thickness=1)
        #########################
        arr=np.array([(x1,y1),(x2,y2),(x3,y3),(x4,y4)])
   

    return  arr,shape


def DoG(img):
    global q
    blur5 = cv2.GaussianBlur(img,(5,5),0)
    blur3 = cv2.GaussianBlur(img,(1,1),0)
    DoGim = blur5 - blur3
    kernelClose = np.ones((3, 3),np.uint8)
    DoGim = cv2.morphologyEx(DoGim, cv2.MORPH_CLOSE, kernelClose)
    cv2.imshow("Dogim",DoGim)
    return DoGim


# In[4]:


def detectShapes(mask,image):
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
    cnts=sorted(cnts, key=cv2.contourArea, reverse=True)
    for c in cnts:
        if cv2.arcLength(c, True)>50:       #this is the condition to eliminate small curves 
            points,shape = detect(c,img,cnts,thresh)
            if (shape == "rectangle"):
                cv2.drawContours(img, c, -1, (0,0,0), 3)
                cv2.imshow("img",img)
    return points

def maincode(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mx = np.amax(gray)
    mn = np.amin(gray)
    thresh_val = np.average(np.arange(mn, mx))
    _, thresh = cv2.threshold(gray, mx-50, 255, cv2.THRESH_BINARY)
    #thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
    color = ""
    pts=detectShapes(thresh,image)
    return pts


    

