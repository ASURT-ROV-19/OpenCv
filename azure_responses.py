

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry, Region
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
import cv2
import numpy as np
from transform import four_point_transform
import requests
import json

#define the counter for the images
i=0

X=20
Y=20

def make_prediction(image2,image,counter):
    triangle=0
    circle=0
    square=0
    line=0

    
    #image will be replaced preodically by the image we want to work on
    # Open the sample image and get back the prediction results.
    with open(image, mode="rb") as test_data:
        response = requests.request("POST", url, headers=headers,data=test_data)
        data=response.json()
    # Display the results.
    for prediction in data['predictions']:

        #, prediction.bounding_box.left, prediction.bounding_box.top, prediction.bounding_box.width, prediction.bounding_box.height
        # you can use those to draw a bounding rectangle
        if(prediction['probability']>0.73):
            if(prediction['tag_name'] == "circle"):
                circle+=1
            elif(prediction['tag_name']== "line"):
                line+=1
            elif(prediction['tag_name'] == "triangle"):
                triangle+=1
            elif(prediction['tag_name'] == "square"):
                square+=1
    
    cv2.putText(image2, str(line), (X, Y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.line(image2, (X + 30, Y - 2), (X + 70, Y - 2), (0, 0, 255), 4)

    cv2.putText(image2, str(circle), (X, Y + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.circle(image2, (X + 40, Y + 35), 15, (0, 0, 255), -1)

    cv2.putText(image2, str(square), (X, Y + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.rectangle(image2, (X + 25, Y + 60), (X + 55, Y + 90), (0, 0, 255), -1)

    pt1 = (X + 40, Y + 100)
    pt2 = (X + 20, Y + 130)
    pt3 = (X + 60, Y + 130)
    triangle_cnt = np.array([pt1, pt2, pt3])
    cv2.drawContours(image2, [triangle_cnt], 0, (0, 0, 255), -1)
    cv2.putText(image2, str(triangle) + " ", (X, Y + 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow("result",image2)
      
    counter+=1
     
    


url = "https://southcentralus.api.cognitive.microsoft.com/customvision/v3.0/Prediction/dbfed461-14c1-4615-b17a-d05db9230f54/detect/iterations/Iteration%2011/image"

headers = {
    'prediction-key': "b48ac6ad4b424b4bb914abc4ee6c8802",
    'content-type': "application/octet-stream",
    'training-key': "f13a5db8bb5c4188a7c2ee7bab1f4b9bf13a5db8bb5c4188a7c2ee7bab1f4b9b",
    'cache-control': "no-cache",
    'postman-token': "8800346d-b5b1-b084-14c6-7a3c01f308d2"
    }

cap = cv2.VideoCapture(0)
###################################
points=[]
point1=(300,300)
point2=(900,300)
point3=(300,600)
point4=(900,600)
###################################
points.append(point1)
points.append(point2)
points.append(point3)
points.append(point4)
###################################
points=np.array(points)


base="frame"
while(1):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    #roi    
    roi =frame[300:600,300:900]
    
    #rectangle
    cv2.rectangle(frame,(300,300),(900,600),(0,255,255),5)

  
    #crop the image
    cv2.circle(frame,(300,300), 10, (255,255,255), -1)
    cv2.circle(frame,(900,300), 10, (255,255,255), -1)
    cv2.circle(frame,(300,600), 10, (255,255,255), -1)
    cv2.circle(frame,(900,600), 10, (255,255,255), -1)




    #imshow
    cv2.imshow("frame",frame)
    cv2.imshow("frame2",roi)

    key=cv2.waitKey(1)
    
    if key & 0xFF == ord('e'):
      warped = four_point_transform(roi, points)
      name=str(base)+str(i)
      cv2.imwrite(name+".png",roi)
      make_prediction(roi,name+".png",i)


      
    elif key & 0xFF == ord('q'):
       break

 

