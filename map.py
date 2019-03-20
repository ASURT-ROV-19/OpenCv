import cv2
import numpy as np
import matplotlib.pyplot as plt

grid = cv2.imread("E:\ROV\Competition\grid2.png")
# img_size = (30*30,40*30)
grid = np.ones(img_size)

# draws the grid for trial purposes
x = grid.shape[1]/4
cv2.line(grid, (x,0), (x,grid.shape[0]), (0, 0, 0), 2)
x = x + grid.shape[1]/4
cv2.line(grid, (x,0), (x,grid.shape[0]), (0, 0, 0), 2)
x = x + grid.shape[1]/4
cv2.line(grid, (x,0), (x,grid.shape[0]), (0, 0, 0), 2)
x = x + grid.shape[1]/4
cv2.line(grid, (x,0), (x,grid.shape[0]), (0, 0, 0), 2)

y = grid.shape[0]/3
cv2.line(grid, (0,y), (grid.shape[1],y), (0, 0, 0), 2)
y = y + grid.shape[0]/3
cv2.line(grid, (0,y), (grid.shape[1],y), (0, 0, 0), 2)
y = y + grid.shape[0]/3
cv2.line(grid, (0,y), (grid.shape[1],y), (0, 0, 0), 2)


print(grid.shape)
cv2.imshow('image', grid)
cv2.imwrite('trial1.png',grid)

cv2.waitKey(0)
cv2.destroyAllWindows()

map = np.array([["down","0"],["right","0"],["up","0"],["right","1"]]) 

mapLength = len(map)
x=0
y=0
x_incrementer = grid.shape[1]/4
y_incrementer = grid.shape[0]/3
for i in range(mapLength):
    if(map[i][0] == "right"):
        x = x + x_incrementer
    elif(map[i][0] == "left"):
        x = x - x_incrementer
    elif(map[i][0] == "down"):
        y = y + y_incrementer
    elif(map[i][0] == "up"):
        y = y - y_incrementer
        
    if(map[i][1] == "1"):
        x = x + x_incrementer/2
        y = y + y_incrementer/2
        break
    i = i+2
	
	measurement = '1.8 cm'
font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (x-3,y-3)
fontScale              = 1
fontColor              = (0,0,255)
lineType               = 2

cv2.putText(grid,measurement, 
    bottomLeftCornerOfText, 
    font, 
    fontScale,
    fontColor,
    lineType)

cv2.imshow('image', grid)
cv2.imwrite('trial1.png',grid)


cv2.waitKey(0)
cv2.destroyAllWindows()
