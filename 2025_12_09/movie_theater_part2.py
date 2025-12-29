import sys
import matplotlib.pylab as plt
import numpy as np

'''
ok so I should break this up a bit better...this is the plan for implementing it tomorrow
the brute-force-ish solution is actually the best here - because we 
just need to follow the boundary of the shape traced out by the red points.
As usual, the problem is stated in
a convenient way to solve this if you just code it up.

So I can implement the following algorithm:

for each pair of red points (pick a pair) - that's O(N^2) but it's not that big since N~500
1) pick a pair of red points - calculate the area (this is fast O(1)) 
2) check if the rectangle is valid, if so save the area if it's larger than max.

to check that the rectangle is valid should be O(N) - so ultimately it's O(N^3) but it should work with 500 points.
points are connected consecutively, so:
identify which lines the rectangle edges lie on. 
Go through points and see if any lines between consecutive points 
intersect the edges of the rectangle. if they do, then we are crossing outside. [there is the special case here of the winding inside, but I will ignore it here since input is not like that, and also this is not intended. I can leave a comment.]
two lines intersect 
1) they have to be perpendicular so:
  line 1: @x1 defined by (s1,e1) in y
  line 2: @y2 defined by (s2,e2) in x
2) they intersect iff x1 in range(s2,e2+1?) AND y2 in range(s1,e1+1?)
    else they don't.

This will be sufficient, but there is another optimization that can be done: 
take into account that the points are incrementally moving...
so in that way, you don't have to check everything and can heavily compress where to look for the intersections. 
but this will run into complications because the shape is non-convex...
so better just leave it alone. 
'''

#check if a particular rectangle is valid. TBD...
def is_rectangle_valid(point1,point2,gpx=None,gpy=None):
    if gpx is None or gpy is None:
        print('please provide valid gpx and gpy')
    x1,y1=point1
    x2,y2=point2
    #bottom left
    x_BL,y_BL=(min(x1,x2),min(y1,y2))
    #top right
    x_TR, y_TR=(max(x1,x2),max(y1,y2))
    x_TR+=1 #tiles are integers, so count correctly.
    y_TR+=1

#connect two consecutive points with the green tiles.
def get_green_connection(point1, point2):
    x1,y1=point1
    x2,y2=point2

    if x1==x2:
        if y1==y2:
            raise ValueError('invalid consequtive points - must have matching x xor y but not both!')
        #green points are between y's
        s,e=(min(y1,y2),max(y1,y2))
        gp_y=np.arange(s,e+1)
        gp_x=np.ones_like(gp_y)*x1
    elif y1==y2:
        #green points are between x's
        s,e=(min(x1,x2),max(x1,x2))
        gp_x=np.arange(s,e+1)
        gp_y=np.ones_like(gp_x)*y1
    else:
        raise ValueError('invalid consequtive points - must have matching x xor y')
    return gp_x, gp_y
#a bit of a clever way to calculate the rectangle area
def getArea(point1, point2):
    x1,y1=point1
    x2,y2=point2
    # #avoid overflow
    # x1=float(x1)
    # x2=float(x2)
    # y1=float(y1)
    # y2=float(y2)
    #bottom left
    x_BL,y_BL=(min(x1,x2),min(y1,y2))
    #top right
    x_TR, y_TR=(max(x1,x2),max(y1,y2))
    x_TR+=1 #tiles are integers, so count correctly.
    y_TR+=1

    return (y_TR-y_BL)*(x_TR-x_BL)

if __name__=="__main__":
    fname=sys.argv[1]

    x_list=[]
    y_list=[]
    with open(fname) as f:
        for line in f:
            l=line.strip().split(',')
            x,y=[int(val) for val in l]
            x_list.append(x)
            y_list.append(y)

    N=len(x_list)
    x=np.array(x_list)
    y=np.array(y_list)

    # # super helpful if you look at the input...
    # plt.plot(x,y)
    # plt.show()

    #first, follow the problem statement, and connect consecutive points
    #with the green tiles. (green tiles will cover the red here)
    gpx=[]
    gpy=[]
    for i in range(N):
        curr_point=(x[i],y[i])
        if i==N-1:
            next_point=(x[0],y[0])
        else:
            next_point=(x[i+1],y[i+1])
        gp_x, gp_y=get_green_connection(curr_point,next_point)
        gpx.extend(gp_x)
        gpy.extend(gp_y)

    gpx=np.array(gpx)
    gpy=np.array(gpy)
    #now we know what is inside, and what is outside.

    #now we can go an calculate areas...

    # calculate all areas (if needed)
    all_areas=np.zeros((N,N),dtype='float64')
    for i in range(N):
     for j in range(i+1,N):
         point1=(x[i],y[i])
         point2=(x[j],y[j])
         all_areas[i,j]=getArea(point1,point2)
    fig,ax=plt.subplots(1,1,figsize=(8,4))
    ax.matshow(all_areas)
    plt.show()
    