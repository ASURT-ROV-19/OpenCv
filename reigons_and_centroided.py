#the central region needs to have red
#if it doesn't have red , this means we are at a corner or we drifted and need to return
    #4#
  #2#1#3#
    #5#

import cv2
import numpy as np
import math
import time
import imutils
import socket
from UDP import UDP_Client

directions=[]

#Define an object from the UDP class
#Target ip is the Pi's address.
#port is the port we are communicating with
udb_socket=UDP_Client("10.1.1.15",9020)


def black_tile_edges(frame):
  frame = imutils.resize(frame, height = 300)
  lower_hue = np.array([0,0,0])
  upper_hue = np.array([255,255,50])
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  mask = cv2.inRange(hsv, lower_hue, upper_hue)
  edges=edge_detect(mask)
  cnts_b,h  = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  if ( len(cnts_b)>0):
    #we detected an edge, means now we are changing tiles
    cnts_b = sorted(cnts_b, key = cv2.contourArea, reverse = True)[:2]
    # we have so far a def. which finds the black contous, moving from this we can count the black we find the screen


def  crack_length_estimaion(frame):
  frame2=blue_filtering(frame)
  blue=blue_amount_in_frames(frame2)
  if( enough_blue(blue) ):
    #edge detect
    res_blue =edge_detect(frame2)
    #contors finding 
    cnts_blue,h  = cv2.findContours(res_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts_blue = sorted(cnts_blue, key = cv2.contourArea, reverse = True)[:2]
    #draw the  blue contor
    cv2.drawContours(frame2, cnts_blue, 0, (255,255,255), 3)
    #Gets the length of biggest contor
    peri = cv2.arcLength(cnts_blue[0], True)
    #Approximates the Contor we have to one with less vertices
    approx = cv2.approxPolyDP(cnts_t[0], 0.02 * peri, True)
    vertices = cv2.convexHull(approx, clockwise=False)
    for corner in vertices:
      x,y=corner[0].ravel()
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
    ###########################
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

    if line1 < line2:
        lin_ref=line1
        pix_lin=line2
    else :
        lin_ref=line2
        pix_lin=line1

    #width of lenth 1.7cm -----> change to 1.8 or 1.9
    len_of_line = (pix_lin * 1.7)/lin_ref
    len_of_line=round(len_of_line, 1)
    len_of_line=str(len_of_line)
  


def enough_red(red_value,threshold):
  if(red_value>threshold):
    return True
  else:
    return False

def enough_blue(blue_value):
  #we need to get the value!
  # number of blue in yara's photo : 14910902
  blue_threshold=14910000
  if(blue_value>blue_threshold):
    return True
  else:
    return False


def centroid_of_frame(frame):
  shape=frame.shape
  frame_height=shape[0]
  frame_width=shape[1]
  frame_height=int(frame_height/2)
  frame_height=int(frame_width/2)
  return frame_height,frame_height


# def red_filtering(img):
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#     min = np.array([0, 100 , 100])
#     max = np.array([179, 250, 250])
#     mask = cv2.inRange(hsv, min, max)
#     res = cv2.bitwise_and(img, img, mask=mask)
#     #blur = cv2.bilateralFilter(res,9,75,75)
#     return res

def red_filtering(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    min = np.array([0, 100 , 0])
    max = np.array([179, 255, 250])
    mask = cv2.inRange(hsv, min, max)
    res = cv2.bitwise_and(img, img, mask=mask)
    #kernelClose = np.ones((5, 5),np.uint8)
    #res = cv2.morphologyEx(res, cv2.MORPH_CLOSE, kernelClose)
    #blur = cv2.bilateralFilter(res,9,75,75)
    return res

def blue_filtering(img):
  hsv_blue = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
  #define lower and upper limit for the blue color
  lower_blue=np.array([110,50,50])
  upper_blue=np.array([130,255,255])
  #define the mask
  mask_blue=cv2.inRange(hsv_blue , lower_blue ,upper_blue)
  #mask the image
  res1= cv2.bitwise_and(img,img,mask=mask_blue)
  return res1

def black_filtering(img):
  lower_hue = np.array([0,0,0])
  upper_hue = np.array([255,255,50])
  



def red_amount_in_frames(pic):
    _s=pic.shape
    height=_s[0]
    width=_s[1]
    constant_error=3315
    red=np.sum(pic[0:height, 0:width])
    red=red-constant_error
    return red

def blue_amount_in_frames(pic):
    _s=pic.shape
    height=_s[0]
    width=_s[1]
    # We need to find the constant error of blue!
    #constant_error=3315
    blue=np.sum(pic[0:height, 0:width])
    return blue

def edge_detect(frame):
  frame = cv2.Canny(frame, 100, 100)
  blur5 = cv2.GaussianBlur(frame,(5,5),0)
  blur3 = cv2.GaussianBlur(frame,(1,1),0)
  return blur5-blur3

def error_founder(points,frame):
  half_height=height/2
  half_width=width/2
  points_testing={"x":half_width,"y":half_height}
  # points_testing=coordiante_fixer("middle",points_testing)
  cv2.circle(frame,(int(points_testing['x']),int(points_testing['y'])), 20, (45,191,255), -1)
  #points_testing=actual_center("middle")
  cv2.line(frame,(int(points_testing['x']),int(points_testing['y'])),(int(points['x']),int(points['y'])),(255,0,0),5)
  error_x=points['x']-points_testing['x']
  error_y=points['y']-points_testing['y']
  return error_x,error_y



def coordiante_fixer(reigon,points):
  #due to we having 5 frames, we will do this to fix the coordiantes
  if(reigon == "top"):

      points['x']=points['x']+(int((width/2))-reigon_half_width)
      points['y']= points['y'] +(int((height/2))-3*reigon_half)
      cv2.circle(frame,(points['x'],points['y']), 5, (0,255,255), -1)


  elif (reigon == "left"):

     points['x']=points['x']+(int((width/2))-3*reigon_half_width)
     points['y']=points['y']+(int((height/2))-reigon_half)
     cv2.circle(frame,(points['x'],points['y']), 5, (0,255,255), -1)

  elif (reigon == "right"):
      points['x']=points['x']+(int((width/2))+reigon_half_width)
      points['y']=points['y']+(int((height/2))-reigon_half)
      cv2.circle(frame,(points['x'],points['y']), 5, (0,255,255), -1)

  elif (reigon=="down"):
    points['x']=points['x']+(int((width/2))-reigon_half_width)
    points['y']=points['y']+(int((height/2))+reigon_half)
    cv2.circle(frame,(points['x'],points['y']), 5, (255,255,255), -1)

  elif(reigon=="middle"):
    points['x']=points['x']+(int((width/2))-reigon_half_width)
    points['y']=points['y']+(int((height/2))-reigon_half)
    cv2.circle(frame,(int(points['x']),int(points['y'])), 5, (255,255,255), -1)

    



  return points



def actual_center(dir):
    ## WE NEED TO ADD A CONDITION TO REMOVE CONTOURS THAT ARE SMALLER THAN A CERTAIN LENGTH
    #actual_centroid of the reigons
    if (dir == "right") or (dir=="rightu") or (dir=="rightd"):
      #right
      try:
         right_cnt = cnts_r[0]
         M_r= cv2.moments(right_cnt)
         cx_r = int(M_r['m10']/M_r['m00'])
         cy_r = int(M_r['m01']/M_r['m00'])
         points_r={"x":cx_r , "y":cy_r}
         cv2.circle(right,(points_r["x"],points_r["y"]), 2, (255,255,255), -1)
         points_r=coordiante_fixer("right",points_r)
         return points_r
      except IndexError:
         points_r={"x":xright,"y":yright}
         points_r=coordiante_fixer("right",points_r)
         
         return points_r

      

    elif(dir == "left") or (dir=="leftu") or (dir=="leftd"):
      #left
      try:
         left_cnt = cnts_l[0]
         M_l= cv2.moments(left_cnt)
         cx_l = int(M_l['m10']/M_l['m00'])
         cy_l = int(M_l['m01']/M_l['m00'])
         points_l={"x":cx_l , "y":cy_l}
         cv2.circle(left,(points_l["x"],points_l["y"]), 2, (255,255,255), -1)
         points_l=coordiante_fixer("left",points_l)
         return points_l
        
      except IndexError:
         points_l={"x":xleft,"y":yleft}
         cv2.circle(left,(points_l["x"],points_l["y"]), 2, (255,255,255), -1)
         points_l=coordiante_fixer("left",points_l)
         return points_l
      
    
    elif (dir == "up") or (dir=="upl") or (dir=="upr"):
      #top
      try:
         top_cnt = cnts_t[0]
         M_t= cv2.moments(top_cnt)
         cx_t = int(M_t['m10']/M_t['m00'])
         cy_t = int(M_t['m01']/M_t['m00'])
         points_t={"x":cx_t , "y":cy_t}
         cv2.circle(top,(points_t["x"],points_t["y"]), 2, (255,255,255), -1)
         points_t=coordiante_fixer("top",points_t)
         return points_t
      except IndexError :
         points_t={"x":xtop,"y":ytop}
         cv2.circle(top,(points_t["x"],points_t["y"]), 2, (255,255,255), -1)
         points_t=coordiante_fixer("top",points_t)
         return points_t
      

    
    elif(dir == "down") or (dir=="downl") or (dir=="downr"):
      #bottom
      try:
         down_cnt = cnts_d[0]
         M_d= cv2.moments(down_cnt)
         cx_d = int(M_d['m10']/M_d['m00'])
         cy_d = int(M_d['m01']/M_d['m00'])
         points_d={"x":cx_d , "y":cy_d}
         cv2.circle(down,(points_d["x"],points_d["y"]), 2, (255,255,255), -1)
         points_d=coordiante_fixer("down",points_d)
         return points_d
      except IndexError:
         points_d={"x":xdown,"y":ydown}
         cv2.circle(down,(points_d["x"],points_d["y"]), 2, (255,255,255), -1)
         points_d=coordiante_fixer("down",points_d)
         return points_d

    elif(dir == "middle"):
      #left
      try:
         mid_cnt = cnts_m[0]
         M_m= cv2.moments(mid_cnt)
         cx_m = int(M_m['m10']/M_m['m00'])
         cy_m = int(M_m['m01']/M_m['m00'])
         points_m={"x":cx_m , "y":cy_m}
         cv2.circle(middle,(points_m["x"],points_m["y"]), 2, (255,255,255), -1)
         points_m=coordiante_fixer("middle",points_m)
         return points_m
        
      except IndexError:
         points_m={"x":xmiddle,"y":ymiddle}
         cv2.circle(middle,(points_m["x"],points_m["y"]), 2, (255,255,255), -1)
         points_m=coordiante_fixer("middle",points_m)
         return points_m

def middle_reference_error(frame):
  #this funcution will return the error between the main middle frame and the centroid of the contour 
  points_testing={"x":xmiddle,"y":ymiddle}
  points_testing=actual_center("middle")
  cv2.circle(frame,(xmiddle,ymiddle), 4, (255,0,0), -1)
  cv2.circle(frame,(int(width/2),int(height/2)),4,(255,255,130),-1)
  middle_x_error=(width/2)-points_testing["x"]
  cv2.line(frame,(points_testing['x'],points_testing['y']),(int(width/2),int(height/2)),(255,255,0),5)

  return  middle_x_error


#def find_biggest_red():

  
      


#cap=cv2.VideoCapture("udpsrc port=5000 ! application/x-rtp,media=video,payload=26,clock-rate=90000,encoding-name=JPEG,framerate=30/1 ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink",cv2.CAP_GSTREAMER)
cap=cv2.VideoCapture(0)
_,_f=cap.read()
shape=_f.shape
height=shape[0]
width=shape[1]
prev=""
nexxt=""

#we need to then divide the frame into 5 main reigons, we select the half length of the reigon
reigon_half=120

reigon_half_width=200

#threshold to say if we have red in this reigon or not
threshold= 600000

while(1):
    
    #flag to check if the middle have a red in it
    middle_flag=1
    time1=time.time()
    # Capture frame-by-frame
    ret, frame = cap.read()

    #flip
    frame = cv2.flip(frame, 1)

    #we need to filter for the color red
    frame=red_filtering(frame)

    #defination of the 5 reigons
    middle  = frame[ int(height/2)-reigon_half:int(height/2)+reigon_half 
                    , int(width/2)-reigon_half_width:int(width/2)+reigon_half_width]

    top     = frame[ int(height/2)-3*reigon_half:int(height/2)-reigon_half 
                    , int(width/2)-reigon_half_width:int(width/2)+reigon_half_width]


    right   = frame[ int(height/2)-reigon_half:int(height/2)+reigon_half 
                    ,int(width/2)+reigon_half_width: int(width/2)+3*reigon_half_width]

    left    = frame[ int(height/2)-reigon_half:int(height/2)+reigon_half 
                    , int(width/2)-3*reigon_half_width:int(width/2)-reigon_half_width]

    down     = frame[int(height/2)+reigon_half:int(height/2)+3*reigon_half 
                    , int(width/2)-reigon_half_width:int(width/2)+reigon_half_width]

    #padding to easier the shape detection
    top     = cv2.copyMakeBorder(top,5,5,5,5,cv2.BORDER_CONSTANT,0)
    middle  = cv2.copyMakeBorder(middle,5,5,5,5,cv2.BORDER_CONSTANT,0)
    right   = cv2.copyMakeBorder(right,5,5,5,5,cv2.BORDER_CONSTANT,0)
    left    = cv2.copyMakeBorder(left,5,5,5,5,cv2.BORDER_CONSTANT,0)
    down    = cv2.copyMakeBorder(down,5,5,5,5,cv2.BORDER_CONSTANT,0)

    #edge detection to find the contour
    top_edged=edge_detect(top)
    middle_edged=edge_detect(middle)
    right_edged=edge_detect(right)
    left_edged=edge_detect(left)
    down_edged=edge_detect(down)
    
    #contour detection in each reigon
    cnts_t,h  = cv2.findContours(top_edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts_t = sorted(cnts_t, key = cv2.contourArea, reverse = True)[:2]
    ##
    cnts_d,h  = cv2.findContours(down_edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts_d = sorted(cnts_d, key = cv2.contourArea, reverse = True)[:2]
    ##
    cnts_r,h  = cv2.findContours(right_edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts_r = sorted(cnts_r, key = cv2.contourArea, reverse = True)[:2]
    ##
    cnts_l,h  = cv2.findContours(left_edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts_l = sorted(cnts_l, key = cv2.contourArea, reverse = True)[:2]
    ##
    cnts_m,h  = cv2.findContours(middle_edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts_m = sorted(cnts_m, key = cv2.contourArea, reverse = True)[:2]
    ##

    #draw the largest contour in each frame
    cv2.drawContours(top, cnts_t, 0, (255,255,255), 3)
    cv2.drawContours(down, cnts_d, 0, (255,255,0), 3)
    cv2.drawContours(right, cnts_r, 0, (0,255,255), 3)
    cv2.drawContours(left, cnts_l, 0, (190,255,30), 3)
    cv2.drawContours(middle, cnts_m, 0, (0,70,0), 3)


    #centroid of the reigon
    xtop,ytop       =centroid_of_frame(top)
    xmiddle,ymiddle =centroid_of_frame(middle)
    xdown,ydown     =centroid_of_frame(down)
    xright,yright   =centroid_of_frame(right)
    xleft,yleft     =centroid_of_frame(left)



    # cv2.circle(top,(xtop,ytop), 2, (0,0,255), -1)
    # cv2.circle(middle,(xmiddle,ymiddle), 2, (255,0,0), -1)
    # cv2.circle(right,(xright,yright), 2, (0,255,0), -1)
    # cv2.circle(left,(xleft,yleft), 2, (170,89,0), -1)
    # cv2.circle(down,(xdown,ydown), 2, (255,255,255), -1)
    
    
    
    #amount of red in each reigon
    red_middle=red_amount_in_frames(middle)
    red_top=red_amount_in_frames(top)
    red_down=red_amount_in_frames(down)
    red_right=red_amount_in_frames(right)
    red_left=red_amount_in_frames(left)


    #decision making part
    if (prev!= ""):
      # we check if middle has red, if so we decision make!
      if( enough_red(red_middle,threshold ) ):
        #we have red in the center
        top_condition = enough_red(red_top,threshold)
        left_condition= enough_red(red_left,threshold)
        right_conditon= enough_red(red_right,threshold)
        down_condition= enough_red(red_down,threshold)

        if (top_condition and down_condition):       
          if(prev=="up"):
             nexxt="up"
             ###################################
            
          elif (prev == "down"):
             nexxt="down"
             ###################################

        elif (right_conditon and left_condition):
          if(prev=="right"):
            nexxt="right"
            ###################################
           
          elif (prev == "left"):
              nexxt="left"
              ###################################

        elif (down_condition and right_conditon):
         
          if (prev=="left"):
            nexxt="down"
            ###################################    

           
          elif(prev=="up"):
            nexxt="right"
            ###################################
            
          
        elif(down_condition and left_condition):
          if(prev=="right"):
            nexxt="down"
            print("entered here2")
            ###################################
           
          elif(prev=="up"):
            print("entered here")
            nexxt="left"
            ###################################
            
            

        elif(top_condition and left_condition):
          if (prev=="right"):
            nexxt="up"
            ###################################
            
          elif (prev=="down"):
            nexxt="left"
            ###################################
          
            
        elif(top_condition and right_conditon):
          if (prev=="down"):
            nexxt="right"
            ###################################
            
          elif(prev=="left"):
            nexxt="up"
            ###################################
        
        ##########Step1-control##################################
        if(prev=="downl"):nexxt="left"
        elif(prev=="downr"):nexxt="right"
        elif(prev=="rightu"):nexxt="up"
        elif(prev=="rightd"):nexxt="down"  
        elif(prev=="leftu"):nexxt="up"     
        elif(prev=="leftd"):nexxt="down"  
        elif(prev=="upl"):nexxt="left"   
        elif(prev=="upr"):nexxt="right"     
        ########################################################
      else:
        
        #this case means there are no red in the middle reigon, so we need to either search for the biggest
        #red contour and then find that error and send it to the PID, if we don't find ANY red, we just simply
        #invert the next state



        #we need to make a conditon to differentatiate the normal nexxt and the nexxt due to a fixed
        #control

        #step 1 , check the surronding frames
        step_1_flag=1
        if(prev=="up" or prev=="down"):
          if(enough_red(red_left,threshold)):
            #go to the contour of the left
            if(prev=="up"):nexxt="rightu"
            elif(prev=="down"):nexxt="rightd"  
            step_1_flag=0

          elif(enough_red(red_right,threshold)):
            #go to the contour of the right
            if(prev=="up"):nexxt="leftu"
            elif(prev=="down"):nexxt="leftd"
            step_1_flag=0
        ###################################    
        elif(prev=="left" or prev=="right"):
          if(enough_red(red_top,threshold)):
            #go to the contour of the left
            if(prev=="left"):nexxt="downl"
            elif(prev=="right"):nexxt="downr"
            step_1_flag=0

          elif(enough_red(red_down,threshold)):
            #go to the contour of the right
            if(prev=="left"):nexxt="upl"
            elif(prev=="right"):nexxt="upr"
            step_1_flag=0
        
        #######TO DO############# FIX STEP 2
        
        # #step 2 , check the frame for ANY red.
        # step_2_flag=1
        
        # if(step_1_flag==1):
        #   print("here")
        #   middle_flag=0
        #   #we didnot find red in any of the surronding rectangles
        #   #let's search the whole frame for red
        #   edged=edge_detect(frame)
        #   cnts_f,h  = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #   cnts_f = sorted(cnts_f, key = cv2.contourArea, reverse = True)[:2]

        #   #let's search for a contour in the frame, if we found one,let's go to it
        #   if(len(cnts_f)>0):
        #       print("am i here?")
        #       frame_cnt = cnts_f[0]
        #       peri = cv2.arcLength(frame_cnt[0], True)
        #       if(peri>500):
        #         print("am i here?2")
        #         cv2.drawContours(frame, cnts_f, 0, (255,255,255), 3)
        #         M_f= cv2.moments(frame_cnt)
        #         cx_f = int(M_f['m10']/M_f['m00'])
        #         cy_f = int(M_f['m01']/M_f['m00'])
        #         points_f={"x":cx_f , "y":cy_f}
        #         step_2_flag=0
                
        #         print("we found something")
     


        #if(step_2_flag==1):
          #we didn't find ANY red , either revert the last state or just move the camera

    else:
          #this makes us continue on the next state
          nexxt=prev
          #The other approach is to just search for red and go to it, this needs testing after applying the forward idea
          
    


    if (prev!="" and middle_flag==1):
      points=actual_center(nexxt)
      errorx,errory=error_founder(points,frame)
      #yao_error=int(middle_reference_error(frame))
      #combines the errors into a string
      #error_string= str(errorx) + "," + str(errory)+ ","+str(yao_error)
      error_string= str(errorx) + "," + str(errory)
      #send the error via a udp socket
  
      #udb_socket.send(error_string)
      
      #print errors
      print("Error in X is "+ str(errorx) )
      print("Error in Y is "+ str(errory) )
      #print("Error in Yao is "+ str(yao_error) )

      print(nexxt)
      #display them
      cv2.putText(frame, "next state is"+str(nexxt),(10, 10),cv2.FONT_HERSHEY_COMPLEX_SMALL,.7,(225,0,0))
      cv2.putText(frame, "error in x is"+str(errorx),(20, 20),cv2.FONT_HERSHEY_COMPLEX_SMALL,.7,(225,0,0))
      cv2.putText(frame, "error in Y is"+str(errory),(30, 30),cv2.FONT_HERSHEY_COMPLEX_SMALL,.7,(225,0,0))
      #cv2.putText(frame, "error in Yao is"+str(yao_error),(40, 40),cv2.FONT_HERSHEY_COMPLEX_SMALL,.7,(225,0,0))

      
      #update the state
      prev=nexxt
      time2=time.time()

      time_total=time2-time1 
      print(time_total)
    # elif(prev!="" and middle_flag==0):
    #   #means we found red somewhere in the frame, and we want to go to it.
    #   #errorx=points_f['x']-width/2
    #   x="a"
    #  # errory=points_f['y']-height/2

    
  
    


    #show the image
    cv2.imshow('f',frame)
    cv2.imshow('top',top)
    cv2.imshow('left',left)
    cv2.imshow('right',right)
    cv2.imshow('down',down)
    cv2.imshow('middle',middle)

  

    key=cv2.waitKey(1)

    if key & 0xFF == ord('u'):
      prev="up"
      
    elif key & 0xFF == ord('q'):
       break

    elif key & 0xFF == ord('d'):
       prev="down"
      
    elif key & 0xFF == ord('r'):
      prev="right"
      
    elif key & 0xFF == ord('l'):
      prev="left"
    



    
    
    
cv2.waitKey(0)
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
