import sys
import matplotlib.pylab as plt
from matplotlib.patches import Rectangle
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
  line 1: @y1 defined by (s1,e1) in x
  line 2: @x2 defined by (s2,e2) in y
2) they intersect iff x2 in range(s1,e1+1?) AND y1 in range(s2,e2+1?)
    else they don't.

This will be sufficient, but there is another optimization that can be done: 
take into account that the points are incrementally moving...
so in that way, you don't have to check everything and can heavily compress where to look for the intersections. 
but this will run into complications because the shape is non-convex...
so better just leave it alone. 
'''

#check if a particular rectangle is valid. 
#rectangle is defined by the two corner points as in getArea from part 1
#return area if it is valid. Else return 0. 
#I am returning zero instead of none because I want to see the matrix at the end.
def rectangle_is_valid(point1,point2,X=None,Y=None):
    if X is None or Y is None:
        raise ValueError('Please provide list of points to get_valid_area')
    N=len(X)

    x1,y1=point1
    x2,y2=point2
    #bottom left 
    #I am thinking here with y axis going up, not downwards like in the problem statement.
    x_BL,y_BL=(min(x1,x2),min(y1,y2))
    #bottom right
    x_BR,y_BR=(max(x1,x2),min(y1,y2))
    #top right
    x_TR, y_TR=(max(x1,x2),max(y1,y2))
    #top left
    x_TL, y_TL=(min(x1,x2),max(y1,y2))

    #these are sides defined as lines
    #line is a 2-tuple of two 2-tuples (points) with  ( (x1,y1),(x2,y2) )
    bottom=((x_BL,y_BL),(x_BR,y_BR))
    right=((x_BR,y_BR),(x_TR,y_TR))
    top=((x_TL,y_TL),(x_TR,y_TR))
    left=((x_BL,y_BL),(x_TL,y_TL))

    isValid=True #innocent until proven guilty
    for i in range(N):
        curr_point=(X[i],Y[i])
        if i==N-1:
            next_point=(X[0],Y[0])
        else:
            next_point=(X[i+1],Y[i+1])

        curr_line=(curr_point,next_point)
        if lines_intersect(bottom,curr_line):
            isValid=False
            break
        elif lines_intersect(right,curr_line):
            isValid=False
            break
        elif lines_intersect(top,curr_line):
            isValid=False
            break
        elif lines_intersect(left,curr_line):
            isValid=False
            break
        else:
            isValid=True

    return isValid

#line is a 2-tuple of two 2-tuples (points) with  ( (x1,y1),(x2,y2) )
def lines_intersect(line_rect, line_tiles):
    s1,e1=line_rect
    s2,e2=line_tiles
    result = False #innocent until proven guilty

    s1x,s1y=s1
    e1x,e1y=e1
    s2x,s2y=s2
    e2x,e2y=e2

    #also check that s2 and e2 coordinates are in increasing order.
    if s2y>e2y:
        s2y,e2y=e2y,s2y
    if s2x>e2x:
        s2x,e2x=e2x,s2x
    
    #not necessary -should be already accounted for.
    # #also check that s1x and e1x are in increasing order.
    # if s1x>e1x:
    #     s1x,e1x=e1x,s1x

    #check if they interesect in all these cases...
    if s2x==e2x and s2y==e2y: #tile line is a point, cannot cross another line
        return result
    elif s1x==e1x and s1y==e1y: #rect line is a point, cannot cross another line
        return result 
    elif s1y==e1y and s2y != e2y: #rect line is horizontal and tile line is vertical
        condition1=( s2x > s1x ) and ( s2x < e1x )
        condition2=( s1y > s2y ) and ( s1y < e2y )
        result=condition1 and condition2
        return result
    elif s1y==e1y and s2y == e2y: #rect line is horizontal and tile line is horizontal
        if s1y == s2y: #if they are on the same line
            condition1= ( s1x < s2x ) or ( s1x > e2x )
            condition2= ( e1x < s2x ) or ( e1x > e2x )
            result = condition1 or condition2
            return result
    elif s1x==e1x and s2x != e2x: #rect line is vertical and tile line is horizontal
        condition2=( s2y > s1y ) and ( s2y < e1y )
        condition1=( s1x > s2x ) and ( s1x < e2x )
        result=condition1 and condition2
        return result
    elif s1x==e1x and s2x == e2x: #rect line is vertical and tile line is vertical
        if s1x == s2x: #if they are on the same line...
            condition1= ( s1y < s2y ) or ( s1y > e2y )
            condition2= ( e1y < s2y ) or ( e1y > e2y )
            result = condition1 or condition2
            return result
    else:
        return result
    #I had to write it like this, otherwise it debugging would have been too hard.
    #I needed to work it out so I worked it out like this here.


#true if pair of points is on a horizontal line, else false.
#pointless for tiles... a single tile is both horizontal AND
# def is_horizontal(point1,point2):
#     x1,y1=point1
#     x2,y2=point2
#     result=None
#     if x1==x2: #then the line is vertical
#         if y1==y2: #unless it's a duplicate.
#             #line is a single point,handle as vertical

#             # raise ValueError('invalid consecutive points - must have matching x xor y but not both!')
#         result=False
#     elif y1==y2: #then the line is horizontal
#         s,e=(min(x1,x2),max(x1,x2))
#         result=True
#     else: #should not come here if you provide consecutive points of the input which makes full circle.
#         raise ValueError('invalid consecutive points - must have matching x xor y')
#     return result

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

#I love writing my "get rect" functions.
def get_rect(point1,point2):
    x1,y1=point1
    x2,y2=point2
    x_BL,y_BL=(min(x1,x2),min(y1,y2))
    #top right
    x_TR, y_TR=(max(x1,x2)+1,max(y1,y2)+1)
    return ((x_BL,y_BL), x_TR-x_BL, y_TR-y_BL)

def get_sides(point1,point2):
    x1,y1=point1
    x2,y2=point2
    #bottom left 
    #I am thinking here with y axis going up, not downwards like in the problem statement.
    x_BL,y_BL=(min(x1,x2),min(y1,y2))
    #bottom right
    x_BR,y_BR=(max(x1,x2),min(y1,y2))
    #top right
    x_TR, y_TR=(max(x1,x2),max(y1,y2))
    #top left
    x_TL, y_TL=(min(x1,x2),max(y1,y2))

    #these are sides defined as lines
    #line is a 2-tuple of two 2-tuples (points) with  ( (x1,y1),(x2,y2) )
    bottom=((x_BL,y_BL),(x_BR,y_BR))
    right=((x_BR,y_BR),(x_TR,y_TR))
    top=((x_TR,y_TR),(x_TL,y_TL))
    left=((x_BL,y_BL),(x_TL,y_TL))

    return bottom,right,top,left

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
    X=np.array(x_list,dtype='float64') #master lists of point coordinates.
    Y=np.array(y_list,dtype='float64')

    # # super helpful if you look at the input...
    # plt.plot(x,y)
    # plt.show()

    plt.ion()
    fig,ax=plt.subplots(figsize=(8,6))
    data0,=ax.plot(X+0.5,Y+0.5,'r.-',linewidth=0.5)
    pt1,=ax.plot([],[],'bo')
    pt2,=ax.plot([],[],'bs')
    ax.set_xlim(0,max(X)+2)
    ax.set_ylim(0,max(Y)+2)
    # ax.set_xticks(np.arange(0,max(X)+2))
    # ax.set_yticks(np.arange(0,max(Y)+2))
    plt.grid(True)

    rect=get_rect((X[0],Y[0]),(X[1],Y[1]))
    R=Rectangle(*rect)
    R.set(color='green',alpha=0.5)
    ax.add_patch(R)
    # calculate areas and check if each of those rectangles is valid.
    all_areas=np.zeros((N,N),dtype='float64')
    final_area=0
    for i in range(N):
        for j in range(i+1,N):
            point1=(X[i],Y[i])
            point2=(X[j],Y[j])
            pt1.set_data([X[i]+0.5],[Y[i]+0.5])
            pt2.set_data([X[j]+0.5],[Y[j]+0.5])
            print(f'points are {point1} and {point2}')
            rect=get_rect(point1,point2)
            print(f'rect is {rect}')
            print(f'with sides {get_sides(point1,point2)}')
            R.set(xy=rect[0],width=rect[1],height=rect[2],color='gray',alpha=0.5)
            #for debugging
            validity=rectangle_is_valid(point1,point2,X=X,Y=Y)
            if validity:
                R.set(color='green',alpha=0.5)
            else:
                R.set(color='red',alpha=0.5)
            all_areas[i,j]=get_area(point1,point2)
            print(f'latest area between points {i} and {j}')
            print(f'with coords {point1} and {point2}')
            print(f'with area {all_areas[i,j]}')
            if all_areas[i,j] > final_area:
                # if rectangle_is_valid(point1,point2,X=X,Y=Y):
                if validity:
                    final_area=all_areas[i,j]
                    print(f'latest LARGEST area between points {i} and {j}')
                    print(f'with coords {point1} and {point2}')
                    print(f'with area {all_areas[i,j]}')
                    # all_areas[i,j]=0
            # plt.pause(0.001)#this is as fast as it goes
            plt.pause(0.05)
            # fig.waitforbuttonpress()
    print('done with the loop')

    print('-'*30)
    print(final_area)
    print('-'*30)
    

    plt.ioff() # Turn off interactive mode at the end
    plt.show() # Keep the final plot window open
    

    
    # fig,ax=plt.subplots(1,1,figsize=(8,4))
    # ax.matshow(all_areas)
    # plt.show()
    # 