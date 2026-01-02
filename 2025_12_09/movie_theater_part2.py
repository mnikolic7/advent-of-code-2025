import sys
import numpy as np

#I have given up on writing my own "contains" function
#it took me too long, and I should do it another time
#it's a good exercise, but I need to practice finishing 
#problems now, instead of solving from scratch.
from shapely.geometry import box, Polygon
from shapely.prepared import prep
from shapely import within


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
    
    points=[]
    for i in range(N):
        points.append((X[i],Y[i]))

    red_tiles=Polygon(points)
    # print(red_tiles)
    # red_tiles=prep(red_tiles)
    # print(red_tiles)


    all_areas=np.zeros((N,N))
    final_area=0
    for i in range(N):
        for j in range(i+1,N):
            x1,y1 = X[i], Y[i] 
            x2,y2 = X[j], Y[j]

            area=get_area((x1,y1),(x2,y2))
            all_areas[i,j]=area

            rect=box(min(x1,x2),min(y1,y2),max(x1,x2),max(y1,y2))
            
            if rect.within(red_tiles):
                if area>final_area:
                    final_area=area

    print('-'*30)
    print(final_area)
    print('-'*30)
    
                    