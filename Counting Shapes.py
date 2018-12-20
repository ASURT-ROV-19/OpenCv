
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


def detectShapes(image, mask):
    res = cv2.bitwise_and(image, image, mask=mask)
    cv2.imshow("Result", res)

    X = 20
    Y = 20
    line = 0
    rectangle = 0
    circle = 0
    triangle = 0
    kernel = np.ones((11, 11), np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    cv2.imshow("Closing", closing)
    edges = cv2.Canny(closing, 100, 200)
    blur = cv2.blur(edges, (5, 5), 1)
    cv2.imshow("edg", edges)
#     lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi / 180, threshold=50, minLineLength=300, maxLineGap=0)
    lines = cv2.HoughLinesP(edges,1,np.pi/180,50,minLineLength=5,maxLineGap=50)

    if (lines is None):
        return
    N = lines.shape[0]
    for i in range(N):
        x1 = lines[i][0][0]
        y1 = lines[i][0][1]
        x2 = lines[i][0][2]
        y2 = lines[i][0][3]
        cv2.line(edges, (x1, y1), (x2, y2), (255, 0, 0), 2)

    mx = np.amax(edges)
    mn = np.amin(edges)

    thresh_val = np.average(np.arange(mn, mx))
    _, thresh = cv2.threshold(edges, thresh_val, 255, cv2.THRESH_BINARY)

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

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
    # cv2.putText(image, str(triangle) + " " + "triangle", (X, Y + 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    pt1 = (X + 40, Y + 100)
    pt2 = (X + 20, Y + 130)
    pt3 = (X + 60, Y + 130)
    triangle_cnt = np.array([pt1, pt2, pt3])
    cv2.drawContours(image, [triangle_cnt], 0, (0, 0, 255), -1)
    cv2.putText(image, str(triangle) + " ", (X, Y + 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


# In[4]:



# In[4]:

cap = cv2.VideoCapture(0)
while True:
    _, image = cap.read()
    # image = cv2.imread('shapes2.jpg')

    ratio = image.shape[0] / float(image.shape[0])
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    color = ""

    lower_black = np.array([0, 0, 0])
    upper_black = np.array([10, 10, 60])
    # lower_black = np.array([0, 0, 0])
    # upper_black = np.array([80, 50, 100])

    mask1 = cv2.inRange(hsv, lower_black, upper_black)
    cv2.imshow("mask1", mask1)
    detectShapes(image, mask1)

    cv2.imshow('image', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# image = cv2.imread('10.jpg')

# ratio = image.shape[0] / float(image.shape[0])
# hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# color = ""

# lower_black = np.array([0, 0, 0])
# upper_black = np.array([180, 255, 30])

# mask1 = cv2.inRange(hsv, lower_black, upper_black)
# cv2.imshow("mask1", mask1)
# detectShapes(image, mask1)

# cv2.imshow('image', image)

# cv2.waitKey(0)
# cv2.destroyAllWindows()

