import cv2
import math
import numpy as py
from Tkinter import *


class popupWindow(object):
    def __init__(self,master):
        top=self.top=Toplevel(master)
        self.l=Label(top,text="Enter reference real length")
        self.l.pack()
        self.e=Entry(top)
        self.e.pack()
        self.b=Button(top,text='Ok',command=self.cleanup)
        self.b.pack()
    def cleanup(self):
        self.value=self.e.get()
        self.top.destroy()

class mainWindow(object):
    def __init__(self,master):
        self.master=master
        self.popup()

    def popup(self):
        self.w=popupWindow(self.master)
        self.master.wait_window(self.w.top)
    def getEntryValue(self):
        return self.entryValue()

    def entryValue(self):
        return self.w.value

class MeasureLength:
    line=[]
    ref=[]
    refCircle=0
    objCircle=0
    imageName=""
    lineLength=0
    refLength=0
    refPixes=0
    linePixes=0
    drawingRef=False
    mButtonDown=False
    img=[]
    root=Tk()
    root.withdraw()
    instantiationFlag=0

    #handles mouse events , right mouse click and drag to draw a line , or mouse scroll click and drag to draw a circle


    def handler (self,event,x,y,flags,param):
        if (event==cv2.EVENT_MOUSEMOVE and self.mButtonDown!=True):
            return        
    
        if event==cv2.EVENT_LBUTTONDOWN or event==cv2.EVENT_MBUTTONDOWN:
            self.mButtonDown=True
            if len(self.ref)==2:
#       REF HAS TWO POINTS , THEN LINE IS WHAT NEEDS TO BE DRAWN                
                self.drawingRef=False
                if len(self.line)<2:
                    self.line=[(x,y)]
                else:
                    self.newLine(self.img,self.ref,self.line)
                    self.line=[(x,y)]
                if (event==cv2.EVENT_MBUTTONDOWN):
                    self.objCircle=True
                else:
                    self.objCircle=False
#       REF IS NOT TWO POINTS , THEN IT SHALL BE DRAWN
            else:
                self.ref=[(x,y)]
                self.drawingRef=True
#       CIRCLE OR LINE ?                
                if (event==cv2.EVENT_MBUTTONDOWN):
                    self.refCircle=True
                else:
                    self.refCircle=False
        
        elif event==cv2.EVENT_LBUTTONUP or event==cv2.EVENT_MBUTTONUP:
            self.mButtonDown=False
            if (self.drawingRef==True):
                m=mainWindow(self.root)
                self.refLength=m.getEntryValue()
                if self.refLength=="":
                    self.refLength=1
                self.refLength=float(self.refLength)
            self.drawingRef=False
        
        elif event==cv2.EVENT_MOUSEMOVE:
            if self.drawingRef==False:
                if len(self.line)<2:
                    self.line.append((x,y))
                elif len(self.line)==2:
                    self.line[1]=(x,y)
            else:
                if len(self.ref)<2:
                    self.ref.append((x,y))
                elif len(self.ref)==2:
                    self.ref[1]=(x,y)
            self.relocateLine(self.ref,self.line)
#            self.newLine(self.img,self.ref,self.line)
            self.img=self.draw(self.img,self.ref,self.line)
            cv2.imshow('img',self.img)




    def setImage(self,image):
        if self.instantiationFlag==0:
            self.instantiationFlag=1
        self.img=image
        cv2.imshow("img",self.img)
        cv2.namedWindow("img")
        cv2.setMouseCallback("img",self.handler)
        cv2.waitKey(0)

    def findImage(self,imageName):
        if self.instantiationFlag==0:
            self.instantiationFlag=1
            self.imageName=imageName
        while True:
            image=cv2.imread(imageName)
            self.img=image
            cv2.imshow("img",self.img)
            cv2.namedWindow("img")
            # cv2.setWindowProperty("img", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.setMouseCallback("img",self.handler)
            cv2.waitKey(0)
            key=cv2.waitKey() & 0xff
            if key==ord('q'):
                break
            elif key==ord('r'):
                self.reset()


    def draw(self,image,ref,line):    
        if (len(line)==2 and len(ref)==2):
            if (self.objCircle==True):
                cv2.circle(image,(line[0][0],line[0][1]),int(self.linePixes),(0,255,0),1)
            cv2.line(image,line[0],line[1],(0,255,0),2)
            self.linePixes=round(math.sqrt(pow(line[0][0]-line[1][0],2)+pow(line[0][1]-line[1][1],2)),3)
            self.lineLength=round(self.linePixes*self.refLength/self.refPixes,3)
            cv2.putText(image,str(self.linePixes)+"/"+str(self.lineLength),(int((line[0][0]+line[1][0])/2),int((line[0][1]+line[1][1])/2)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        if (len(ref)==2 and len(line)<2):
            if (self.refCircle==True):
                cv2.circle(image,(int((ref[0][0]+ref[1][0])/2),int((ref[0][1]+ref[1][1])/2)),int(self.refPixes/2),(255,100,255),1)
                cv2.circle(image,(int((ref[0][0]+ref[1][0])/2),int((ref[0][1]+ref[1][1])/2)),7,(0,0,255),-1)
            cv2.line(image,ref[0],ref[1],(255,100,255),2)
            self.refPixes=round(math.sqrt(pow(ref[0][0]-ref[1][0],2)+pow(ref[0][1]-ref[1][1],2)),3)
            cv2.putText(image,str(self.refPixes)+"/"+str(self.refLength)+"CM",(int((ref[0][0]+ref[1][0])/2),int((ref[0][1]+ref[1][1])/2)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0, 255), 2)
        return image
    
    def relocateLine(self,ref,line):
        self.img=cv2.imread(self.imageName)
        if (self.drawingRef==False):            
            cv2.line(self.img,ref[0],ref[1],(255,100,255),2)
            if self.refCircle==True:
                cv2.circle(self.img,(int((ref[0][0]+ref[1][0])/2),int((ref[0][1]+ref[1][1])/2)),int(self.refPixes/2),(255,100,255),1)
                cv2.circle(self.img,(int((ref[0][0]+ref[1][0])/2),int((ref[0][1]+ref[1][1])/2)),7,(0,0,255),-1)
                self.refPixes=round(math.sqrt(pow(ref[0][0]-ref[1][0],2)+pow(ref[0][1]-ref[1][1],2)),3)
            cv2.putText(self.img,str(self.refPixes)+"/"+str(self.refLength)+"CM",(int((ref[0][0]+ref[1][0])/2),int((ref[0][1]+ref[1][1])/2)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0, 255), 2)
        
    def newLine(self,image,ref,line):
        line=[]
        self.img=cv2.imread(self.imageName)
        cv2.line(self.img,ref[0],ref[1],(255,100,255),2)
        if self.refCircle==True:
            cv2.circle(image,(int((ref[0][0]+ref[1][0])/2),int((ref[0][1]+ref[1][1])/2)),int(self.refPixes/2),(255,100,255),1)
            cv2.circle(image,(int((ref[0][0]+ref[1][0])/2),int((ref[0][1]+ref[1][1])/2)),7,(0,0,255),-1)
        self.refPixes=round(math.sqrt(pow(ref[0][0]-ref[1][0],2)+pow(ref[0][1]-ref[1][1],2)),3)
        cv2.putText(self.img,str(self.refPixes)+"/"+str(self.refLength)+"CM",(int((ref[0][0]+ref[1][0])/2),int((ref[0][1]+ref[1][1])/2)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0, 255), 2)


    def reset(self):
        self.line=[]
        self.ref=[]
        self.refLength=0
        self.img=cv2.imread(self.imageName)

    def destructor(self):
        self.line=[]
        self.ref=[]
        self.imageName=""
        self.lineLength=0
        self.refLength=0
        self.refPixes=0
        self.linePixes=0
        self.img=[]
        self.instantiationFlag=0
        self.img=cv2.imread(self.imageName)
        cv2.destroyAllWindows()
        


analyzer=MeasureLength()
x=input("Please enter the name of the pic")
analyzer.findImage(str(x)+".jpg")