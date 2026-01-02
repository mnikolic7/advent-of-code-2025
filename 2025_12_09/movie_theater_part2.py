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

    x_starts=np.zeros(np.max(Y)-1)
    x_ends=np.zeros_like(x_starts)
    for i in range()


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
    
                    