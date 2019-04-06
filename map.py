import cv2
import numpy as np
import matplotlib.pyplot as plt


#draws the grid lines
# grid = cv2.imread("E:\ROV\Competition\grid2.png")
img_size = (30*20,40*20,3)
grid = np.ones(img_size)
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
# cv2.imshow('image', grid)
cv2.imwrite('trial1.png',grid)

cv2.waitKey(0)
cv2.destroyAllWindows()

map = np.array([["up","0"],["left","0"],["left","0"],["left","0"],["up","0"],["right","0"],["right","1"],["right","0"],["up","0"]]) 

grids = np.array([["down","right","right","right","down","left","left","left","down","right","right","right","down","1","1"], #grid1_1
				["up","left","left","left","up","right","right","right","up","left","left","left","up","2","3"], 	#grid1_2
				["down","down","down","right","up","up","right","down","down","right","up","up","up","3","1"],	#grid2_1
				["down","down","down","left","up","up","left","down","down","left","up","up","up","4","2"],	#grid2_2
				["right","right","right","right","down","left","left","left","down","right","right","right","right","5","1"],	#grid3_1
				["left","left","left","left","up","right","right","right","up","left","left","left","left","6","3"],	#grid3_2
				["right","down","down","right","up","up","right","down","down","right","up","up","left","7","1"],	#grid4_1
				["left","down","down","left","up","up","left","down","down","left","up","up","left","8","2",], #grid4_2
				["right","right","right","right","down","left","left","left","down","right","right","right","down","9","1"], #grid5_1
				["up","left","left","left","up","right","right","right","up","left","left","left","left","10","3"], #grid5_2
				["right","down","down","right","up","up","right","down","down","right","up","up","up","11","1",],	#grid6_1
				["down","down","down","left","up","up","left","down","down","left","up","up","left","12","2",]])	 #grid6_2

#The last element in each array is the place where it started:
# 1--> top left corner
# 2--> top right corner  
# 3--> bottom right corner 

# The element before the last is just the number of the grid

def calc_matches(grid,mapp,j):
    match = 0
    for i in range(mapp.shape[0]):
        if(grid[i] == mapp[i][0]):
            match = match + 1
            #print match
            
    return grid[len(grid)-2],match
	
max_matches = 0
max_grid_number = 0
for j in range(12):
    grid_number,matches = calc_matches(grids[j],map,j)
    if(matches > max_matches):
        max_matches = matches
        max_grid_number = grid_number   

mapLength = len(map)
x_incrementer = grid.shape[1]/4
y_incrementer = grid.shape[0]/3

grid_number = int(max_grid_number) - 1
start = grids[grid_number][14]

if(start == "1"):
    x=0
    y=0
elif(start == "3"):
    x = grid.shape[1]
    y = grid.shape[0]
elif(start == "2"):
    x = grid.shape[1]
    y = 0

print "at start x =" ,x , " y = ", y
for i in range(1,mapLength):
    if(map[i][0] == "right"):
        x = x + x_incrementer
        print "now in right x =" ,x , " y = ", y 
    elif(map[i][0] == "left"):
        x = x - x_incrementer
        print "now in left x =" ,x , " y = ", y
    elif(map[i][0] == "down"):        
        y = y + y_incrementer
        print "now in down x =" ,x , " y = ", y
    elif(map[i][0] == "up"):
        y = y - y_incrementer
        print "now in up x =" ,x , " y = ", y
        
    if(map[i][1] == "1"):
        if(start == "1"):
            x = x + x_incrementer/2
            y = y + y_incrementer/2
        elif(start == "3"):
            x = x - x_incrementer/2
            y = y - y_incrementer/2
        elif(start == "2"):
            x = x - x_incrementer/2
            y = y + y_incrementer/2
       
        break
    i = i+2
	
measurement = '1.8 cm'
font                   = cv2.FONT_HERSHEY_PLAIN
bottomLeftCornerOfText = (x-3,y-3)
fontScale              = 1
fontColor              = (0,255,255)
lineType               = 2

cv2.putText(grid,measurement, 
    bottomLeftCornerOfText, 
    font, 
    fontScale,
    fontColor,
    lineType)

# cv2.circle(grid,(x,y), 10, (0,255,0), -1)

cv2.imshow('image', grid)
cv2.imwrite('trial1.png',grid)


cv2.waitKey(0)
cv2.destroyAllWindows()
