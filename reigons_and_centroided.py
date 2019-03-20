#the central region needs to have red
#if it doesn't have red , this means we are at a corner or we drifted and need to return
    #4#
  #2#1#3#
    #5#

import cv2
import numpy as np
import math
import time

def enough_red(red_value,threshold):
  if(red_value>threshold):
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


def red_filtering(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    min = np.array([0, 100 , 100])
    max = np.array([179, 250, 250])
    mask = cv2.inRange(hsv, min, max)
    res = cv2.bitwise_and(img, img, mask=mask)
    #blur = cv2.bilateralFilter(res,9,75,75)
    return res

def red_amount_in_frames(pic):
    _s=pic.shape
    height=_s[0]
    width=_s[1]
    constant_error=3315
    red=np.sum(pic[0:height, 0:width])
    red=red-constant_error
    return red

def edge_detect(frame):
  frame = cv2.Canny(frame, 100, 100)
  blur5 = cv2.GaussianBlur(frame,(5,5),0)
  blur3 = cv2.GaussianBlur(frame,(1,1),0)
  return blur5-blur3

def error_founder(points,frame):
  #half_height=height/2
  #half_width=width/2
  points_testing={"x":xmiddle,"y":ymiddle}
  points_testing=actual_center("middle")
  cv2.line(frame,(int(points_testing['x']),int(points_testing['y'])),(int(points['x']),int(points['y'])),(255,0,0),5)
  error_x=points['x']-points_testing['x']
  error_y=points['y']-points_testing['y']
  return error_x,error_y



def coordiante_fixer(reigon,points):
  #due to we having 5 frames, we will do this to fix the coordiantes
  if(reigon == "top"):

      points['x']=points['x']+(int((width/2))-reigon_half)
      points['y']= points['y'] +(int((height/2))-3*reigon_half)
      cv2.circle(frame,(points['x'],points['y']), 5, (0,255,255), -1)


  elif (reigon == "left"):

     points['x']=points['x']+(int((width/2))-3*reigon_half)
     points['y']=points['y']+(int((height/2))-reigon_half)
     cv2.circle(frame,(points['x'],points['y']), 5, (0,255,255), -1)

  elif (reigon == "right"):
      points['x']=points['x']+(int((width/2))+reigon_half)
      points['y']=points['y']+(int((height/2))-reigon_half)
      cv2.circle(frame,(points['x'],points['y']), 5, (0,255,255), -1)

  elif (reigon=="down"):
    points['x']=points['x']+(int((width/2))-reigon_half)
    points['y']=points['y']+(int((height/2))+reigon_half)
    cv2.circle(frame,(points['x'],points['y']), 5, (255,255,255), -1)

  elif(reigon=="middle"):
    print("yara gat hena")
    points['x']=points['x']+(int((width/2))-reigon_half)
    points['y']=points['y']+(int((height/2))-reigon_half)
    cv2.circle(frame,(points['x'],points['y']), 5, (255,255,255), -1)

    



  return points



def actual_center(dir):

    #actual_centroid of the reigons
    if (dir == "right"):
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

      

    elif(dir == "left"):
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
      
    
    elif (dir == "up"):
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
      

    
    elif(dir == "down"):
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
         cv2.circle(left,(points_m["x"],points_m["y"]), 2, (255,255,255), -1)
         points_m=coordiante_fixer("middle",points_m)
         return points_m
        
      except IndexError:
         points_m={"x":xmiddle,"y":ymiddle}
         cv2.circle(middle,(points_m["x"],points_m["y"]), 2, (255,255,255), -1)
         points_m=coordiante_fixer("middle",points_m)
         return points_m

  
      


cap = cv2.VideoCapture(0)
_,_f=cap.read()
shape=_f.shape
height=shape[0]
width=shape[1]
prev=""
nexxt=""

#we need to then divide the frame into 5 main reigons, we select the half length of the reigon
reigon_half=70
#threshold to say if we have red in this reigon or not
threshold= 800000

while(1):
    

    # Capture frame-by-frame
    ret, frame = cap.read()

    #flip
    frame = cv2.flip(frame, 1)

    #we need to filter for the color red
    frame=red_filtering(frame)

    #defination of the 5 reigons
    middle  = frame[ int(height/2)-reigon_half:int(height/2)+reigon_half 
                    , int(width/2)-reigon_half:int(width/2)+reigon_half]

    top     = frame[ int(height/2)-3*reigon_half:int(height/2)-reigon_half 
                    , int(width/2)-reigon_half:int(width/2)+reigon_half]


    right   = frame[ int(height/2)-reigon_half:int(height/2)+reigon_half 
                    ,int(width/2)+reigon_half: int(width/2)+3*reigon_half]

    left    = frame[ int(height/2)-reigon_half:int(height/2)+reigon_half 
                    , int(width/2)-3*reigon_half:int(width/2)-reigon_half]

    down     = frame[int(height/2)+reigon_half:int(height/2)+3*reigon_half 
                    , int(width/2)-reigon_half:int(width/2)+reigon_half]

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
             points=actual_center("down")
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
            ###################################
           
          elif(prev=="up"):
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
            
        
      
    else:
          #this makes us continue on the next state
          next=prev
          #The other approach is to just search for red and go to it, this needs testing after applying the forward idea
          

    if (prev!=""):
      points=actual_center(nexxt)
      errorx,errory=error_founder(points,frame)
      print("Error in X is "+ str(errorx) )
      print("Error in Y is "+ str(errory) )

      prev=nexxt
    
  
    



    #show the image
    cv2.imshow('f',frame)
    cv2.imshow('top',top)
    cv2.imshow('left',left)
    cv2.imshow('right',right)
    cv2.imshow('down',down)
    cv2.imshow('middle',middle)

    #print(nexxt)

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
