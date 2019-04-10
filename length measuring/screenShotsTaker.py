import lengthMeasure
import cv2
import numpy as np

DIM=(1920, 1080)
K=np.array([[1047.318940937412, 0.0, 930.9239255603386], [0.0, 1014.8897353387252, 620.5599097517337], [0.0, 0.0, 1.0]])
D=np.array([[-0.16011193049708344], [0.09630296168771128], [-0.13357796891302956], [0.07161533033816428]])
i=0

def undistort(img_path):

    h,w = img_path.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img_path, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return (undistorted_img)

# FOR STREAMING FROM PORT
cap=cv2.VideoCapture("udpsrc port=5000 ! application/x-rtp,media=video,payload=26,clock-rate=90000,encoding-name=JPEG,framerate=30/1 ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink",cv2.CAP_GSTREAMER);

# cap=cv2.VideoCapture(0)
analyzer=lengthMeasure.MeasureLength()
#imageName="frame.jpg"
# cv2.namedWindow("stream",cv2.WND_PROP_FULLSCREEN)
# cv2.setWindowProperty("stream", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
while True:
    ret,frame=cap.read()
    key=cv2.waitKey(1) & 0xff
    if(ret==1):
        #frame=undistort(frame)
        cv2.imshow("stream",frame)

    if key==ord('s'):
        print("screenshoot taking")
        if(ret==1):
	    imageName="/home/abdelrahman/ASURT/dummyPics/frame"+str(i)+".jpg"
            cv2.imwrite(imageName,frame)
            cv2.destroyWindow("stream")
            i=i+1
        continue

    elif key==ord('q'):
        print("breaking")
        break

cv2.destroyAllWindows()
cap.release()
