
# coding: utf-8

# In[1]:


import cv2
import imutils
import numpy as np


# In[2]:


def detect(c):
    approx = cv2.approxPolyDP(c, 0.04 * cv2.arcLength(c, True), True)
    shape = ''
    if len(approx) == 3:
        shape = "triangle"
        # print(shape)

    elif len(approx) == 4:
        shape = "rectangle"
        # print(shape)

    elif len(approx) == 2:
        shape = "line"
        # print(shape)

    else:
        shape = "circle"
        # print(shape)

    return shape


# In[3]:


def DoG(img):
    blur5 = cv2.GaussianBlur(img,(5,5),0)
    blur3 = cv2.GaussianBlur(img,(3,3),0)
    DoGim = blur5 - blur3
    return DoGim


# In[4]:


def detectShapes(mask):


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
    temp = closing[30:R-30,30:C-30]
    edges =DoG(temp)
    cv2.imshow("edg", edges)
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

    thresh_val = np.average(np.arange(mn, mx))
    _, thresh = cv2.threshold(edges, thresh_val, 255, cv2.THRESH_BINARY)
    
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    
    
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
            shape = detect(c)
            if (shape == "triangle"):
                triangle += 1
            elif (shape == "circle"):
                circle += 1
            elif (shape == "rectangle"):
                rectangle += 1
            elif (shape == "line"):
                line += 1

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


# In[ ]:


cap = cv2.VideoCapture(0)
while True:
    for i in range(15):
         cap.grab()
    (grabbed, image) = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    mx = np.amax(gray)
    mn = np.amin(gray)

    thresh_val = np.average(np.arange(mn, mx))
    _, thresh = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
    color = ""
    detectShapes(thresh)
    cv2.imshow('image', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

# image = cv2.imread('10.jpg')

# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# mx = np.amax(gray)
# mn = np.amin(gray)

# thresh_val = np.average(np.arange(mn, mx))
# _, thresh = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
# color = ""

# cv2.imshow("thresh",thresh)
# detectShapes(image, thresh)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

