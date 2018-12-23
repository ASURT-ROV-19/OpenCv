import cv2
import math
import numpy as np


''' ==========================
white circle is end

dark  is start



 ============================ '''

def next_state_finder(start,end,prev,zawya):

    #For Case of going up

    if (prev=="up"):
        if (zawya>80 and zawya <100):
            next="up"
        elif (zawya>100):
            next="left"
        elif (zawya<80):
            next="right"
        else:
            print("how did this happen")
    
    #For Case of going down

    elif (prev=="down"):
        if (zawya>80 and zawya <100):
            next="down"
        elif (zawya>100):
            next="left"
        elif (zawya<80):
            next="right"
        else:
            print("how did this happen")
    
    #For Case of going right

    elif (prev=="right"):
        if  (zawya<30):
            next="right"
        elif (end['y']<start['y']):
            next="up"
        elif (end['y']>start['y']):
            next="down"
        else:
            print("how did this happen")

     #For Case of going left     

    elif (prev=="left"):
        
        if  (zawya>160):
            next="left"
        elif (end['y']<start['y']):
            next="up"
        elif (end['y']>start['y']):
            next="down"
        else:
            print("how did this happen")

    print(next)
    return next 
 





def end_point_finder(vertices,startpoint):
    max_distance=0
    flag=1
    end_x=0
    end_y=0
    for corner in vertices:
        x,y=corner[0].ravel()
        distance=math.hypot( (startpoint['x'] - x ) , (startpoint['y'] - y ) )
        
        if flag==1:
            max_distance=distance
            flag=0
            end_x=x
            end_y=y

        elif flag==0:
            if (distance>max_distance):
                max_distance=distance
                end_x=x
                end_y=y
    return end_x , end_y







#Cosine_Law 
def cosine_law(start,end):
 
       
    horizontal={"x": 1000 , "y": start["y"] }

    diff_x_start=(1000 - start["x"])
    diff_y_start=0

    diff_x_end=(end["x"]-start["x"])
    diff_y_end=(end["y"]-start["y"])

    adotb= (diff_x_start*diff_x_end) + (diff_y_start*diff_y_end)

   

    a_mag=math.hypot(diff_x_start,diff_y_start)
    b_mag=math.hypot(diff_x_end,diff_y_end)
    cos= (adotb/(a_mag * b_mag))
    angle=math.acos(cos)
    
    return  angle * (180/3.14)


#Testing Purposes

previous="up"
current= 0
startpoint=0
endpoint=0
first_time=1
img = cv2.imread("test37.png", cv2.IMREAD_COLOR)
# detect red lines
# =======================================
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
min = np.array([150, 40, 40])
max = np.array([190, 255, 255])
mask = cv2.inRange(hsv, min, max)
res = cv2.bitwise_and(img, img, mask=mask)

gray_res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
kernal = np.ones((5, 5), np.uint8)
gray_res = cv2.morphologyEx(gray_res, cv2.MORPH_CLOSE, kernal)
# =======================================

# ============ get edges =======================
edges = cv2.Canny(gray_res, 100, 100)
# =============================================

#Detects the contors in the image
_,cnts,h  = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#Sorts them by area
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
#Gets the length of biggest contor
peri = cv2.arcLength(cnts[0], True)
#Approximates the Contor we have to one with less vertices
approx = cv2.approxPolyDP(cnts[0], 0.02 * peri, True)
#same thing
#check the documentation:
#https://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html
vertices = cv2.convexHull(approx, clockwise=False)

#we define variables , called Biggest X, Biggest Y , Smallest X , Smallest Y
smallest_x,smallest_y=vertices[0].ravel()
biggest_x=smallest_x
biggest_y=smallest_y

i=0

for corner in vertices:
    #print(corner)
    x,y=corner[0].ravel()

    if(first_time==1):
        x_smallesty=x
        x_biggesty=x
        y_smallestx=y
        y_biggestx=y
        first_time=0

    
    if (x > biggest_x):
        biggest_x = x
        y_biggestx=y

    elif (x < smallest_x):
        smallest_x = x
        y_smallestx=y

    if (y > biggest_y):
        biggest_y = y
        x_biggesty =x

    elif (y < smallest_y):
        smallest_y = y
        x_smallesty=x

    i+=1

#==================================
#we want to make the rov able to find the next state 
#from the value of the previous state
#==================================
#print(vertices)
next=0

if (previous == "left"):

    startpoint= {"x":biggest_x,"y":y_biggestx}
    cv2.circle(img,(startpoint['x'],startpoint['y']), 10, (100,100,50), -1)
    endx,endy=end_point_finder(vertices,startpoint)
    cv2.circle(img,(endx,endy),10, (255,255,255), -1)
    endpoint={"x": endx,"y": endy}
    zawya= cosine_law(startpoint,endpoint)
    next = next_state_finder (startpoint,endpoint,previous,zawya)
    

    

elif (previous == "right"):
    startpoint= {"x": smallest_x,"y": y_smallestx}
    cv2.circle(img,(startpoint['x'],startpoint['y']), 10, (100,100,50), -1)
    endx,endy=end_point_finder(vertices,startpoint)
    endpoint={"x": endx,"y": endy}
    cv2.circle(img,(endx,endy), 10, (255,255,255), -1)
    zawya= cosine_law(startpoint,endpoint)
    next = next_state_finder (startpoint,endpoint,previous,zawya)



elif (previous == "up"):
    startpoint= {"x":x_biggesty,"y": biggest_y}
    cv2.circle(img,(startpoint['x'],startpoint['y']), 10, (100,100,50), -1)
    endx,endy=end_point_finder(vertices,startpoint)
    endpoint={"x": endx,"y": endy}
    cv2.circle(img,(endx,endy), 10, (255,255,255), -1)
    zawya= cosine_law(startpoint,endpoint)
    next = next_state_finder (startpoint,endpoint,previous,zawya)


elif (previous == "down"):
    startpoint= {"x":x_smallesty,"y":smallest_y}
    cv2.circle(img,(startpoint['x'],startpoint['y']), 10, (100,100,50), -1)
    endx,endy=end_point_finder(vertices,startpoint)
    cv2.circle(img,(endx,endy), 10, (255,255,255), -1)
    endpoint={"x": endx,"y": endy}
    zawya= cosine_law(startpoint,endpoint)
    next = next_state_finder (startpoint,endpoint,previous,zawya)
    











cv2.imshow('Corner', img)


u = cv2.waitKey(0)