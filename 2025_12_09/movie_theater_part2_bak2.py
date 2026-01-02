import sys
import matplotlib.pylab as plt
from matplotlib.patches import Rectangle
import numpy as np

#calculate the rectangle area, leftover from part 1
def get_area(point1, point2):
    x1,y1=point1
    x2,y2=point2
    #bottom left
    x_BL,y_BL=(min(x1,x2),min(y1,y2))
    #top right
    x_TR, y_TR=(max(x1,x2),max(y1,y2))
    x_TR+=1 #tiles are integers, so count correctly.
    y_TR+=1
    area= (y_TR-y_BL)*(x_TR-x_BL)
    return area

def sign(x):
    return ( int(x>0) - int(x<0) ) 

def boundary_cuts(boundary, point1, point2):
    x1,y1=point1
    x2,y2=point2
    #bottom left 
    #I am thinking here with y axis going up, not downwards like in the problem statement.

    bottom=min(y1,y2)
    left=min(x1,x2)
    right=max(x1,x2)+1
    top=max(y1,y2)+1


    bp1,bp2=boundary
    #I checked the input, the boundaries alternate nicely between horizontal and vertical, and the shortest one is of length 7, so I will ignore all weird edge cases that don't happen, in the interest of time. 

    print('*'*20)
    if bp1[0]==bp2[0]:
        boundary_orientation=1 #vertical
        print('vertical')
    elif bp1[1]==bp2[1]:
        boundary_orientation=0 #horizontal
        print('horizontal')
    else:
        print('boundary is invalid invalid!')
        print(f'boundary at points {bp1} and {bp2}')


    result=None
    if boundary_orientation==0: #if boundary is horizontal
        #check if it cuts across the left or right
        #first see if the y position of the boundary is in the middle of the bottom and top, not inclusive
        if ( bp1[1] > bottom ) and (bp1[1] < top):
            #then check that the end points are on opposite sides of left
            print('vertical position is within bounds, check the rest')
            # for left:
            if sign(bp1[0]-left)==-1:
                if sign(bp2[0]-left)>-1:
                    #WE HAVE A CROSS
                    result=True
                    print('cuts left')
                else:
                    result=False
            elif sign(bp1[0]-left)>=0:
                if sign(bp2[0]-left)<0:
                    result=True
                    print('cuts left 2')
                else:
                    result=False
            # for right   
            if sign(bp1[0]-right)<=0:
                if sign(bp2[0]-right)>0:
                    #WE HAVE A CROSS
                    result=True
                    print('cuts right')
                else:
                    result=False
            elif sign(bp1[0]-right)==1:
                if sign(bp2[0]-right)<1:
                    result=True
                    print('cuts right 2')
                else:
                    result=False 
    else: #boundary is vertical
        #first see if the x position of the boundary is in the middle of the left and right, not inclusive
        if ( bp1[0] > left ) and (bp1[0] < right):
            # for bottom:
            if sign(bp1[1]-bottom)==-1:
                if sign(bp2[1]-bottom)>-1:
                    #WE HAVE A CROSS
                    result=True
                    print('cuts bottom')
                else:
                    result=False
            elif sign(bp1[1]-bottom)>=0:
                if sign(bp2[1]-bottom)<0:
                    result=True
                    print('cuts bottom 2')
                else:
                    result=False
            # for top   
            if sign(bp1[1]-top)<=0:
                if sign(bp2[1]-top)>0:
                    #WE HAVE A CROSS
                    result=True
                    print('cuts top')
                else:
                    result=False
            elif sign(bp1[1]-top)==1:
                if sign(bp2[1]-top)<1:
                    result=True
                    print('cuts top2')
                else:
                    result=False

    print(f'sides are y:{bottom}, x:{right}, y:{top}, x:{left} (b r t l)')
    print(f'boundary is {bp1}, {bp2}')
    print(f'sides-bp1 are y:{bottom-bp1[1]}, x:{right-bp1[0]}, y:{top-bp1[1]}, x:{left-bp1[0]} (b r t l)')
    print(f'sides-bp2 are y:{bottom-bp2[1]}, x:{right-bp2[0]}, y:{top-bp2[1]}, x:{left-bp2[0]} (b r t l)')
    
    print(f'result is {result}')
    print('-'*20)
    return result

if __name__=="__main__":
    fname=sys.argv[1]

    X=[]
    Y=[]
    with open(fname) as f:
        for line in f:
            l=line.strip().split(',')
            x,y=[int(val) for val in l]
            X.append(x)
            Y.append(y)

    N=len(X)
    X=np.array(X,dtype='float64') #master lists of point coordinates.
    Y=np.array(Y,dtype='float64')


    final_area=0
    for i in range(N):
        for j in range(i+1,N):
            point1=(X[i],Y[i])
            point2=(X[j],Y[j])

            area=get_area(point1,point2)

            rectangle_bad=False
            for k in range(N):
                b_point1=(X[k],Y[k])
                if k==N-1:
                    b_point2=(X[0],Y[0])
                else:
                    b_point2=(X[k+1],Y[k+1])

                boundary=(b_point1,b_point2)
                if boundary_cuts(boundary, point1, point2):
                    rectangle_bad=True
                    break
            if rectangle_bad:
                break
            else:
                if area>final_area:
                    final_area=area

    print('-'*30)
    print(final_area)
    print('-'*30)
    
                    