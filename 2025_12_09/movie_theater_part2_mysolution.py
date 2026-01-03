import sys
import matplotlib.pylab as plt
import numpy as np
'''
Here is a general plan for the future implementation of "contains"
1-Define a rectangle as bottom, right, top, left (4 integers).
    Shrink them by 1, to exclude the edge which may be intercepted by the boundary curve.
        so bottom and left +=1,
        right and top += 0.
    e.g. if the left is 7 and right is 11:
        leftmost tile is (7-8), so a boundary curve being at < 8 is ok.
        rightmost tile is  (11-12), so a boundary at >11 is ok.
2(optional): check that the bounding box of the curve overlaps with the rectangle.
    this is unnecessary for this problem because by definition it does. 
    but for a general case, if it didn't we could break and save time.
3(optional)Run through the curve once and calculate the winding number at each point.
    To calculate winding number look at current, next and previous point.
        curr=point[i]; next=point[(i+1)%N]; prev=point[(i-1)%N]
        get sign(next-curr) as well as if it is horizontal or vertical.
        get sign(curr-next) as well as if it is horizontal or vertical.
        from that figure out whether at this point the rotation is +90deg or -90deg.
        sum up all the angles for all the points and see if it is +360 or -360.
            I actually checked this and for my input it is +360 and the winding number is 
            randomly changing but never more than (5*90)
4-run through all the points. For each point:
    a. check that the point is not inside the rectangle:
        point.x < left or point.x > right or point.y < bottom or point.y > top
        keep track of where it is relative to the rectangle: north, west, east, south?
        it could also be northwest, southwest, northeast and southeast - in those cases all is good. 
            If it is inside -break, reject rectangle
    b. find the next point and where it is relative to the rectangle
        next.x < left or next.x > right etc...
        make sure that the next point is also on the same side of the rectangle.
        so if next.x > right (the point is on the west),
            then curr point: point.x better be > right (also on the west)
            otherwise check whether the points are also above or below the rectangle.
                if they are, continue
                if they are not - the rectangle is cut by the line.
        since all the connections between points are either horizontal and vertical
        in our case no point goes at any other angle - the curve must go through corner sides (NW, NE, SE, SW) 
        before switching directions. 
    In summary: for each point find whether it is H: East , hor_inside, or West
                also find whether it is           V: South, ver_inside, or North

                check the same for the next point and:
                    first check for point and next that 
                    not (hor_inside and ver_inside) is true for both points
                    i.e. neither point is inside the rectangle. 
                if they are not inside then,
                make sure that their connection doesn't cut the rectangle:
                check that either of these is true:
                    that H value is the same for both points
                    or if not, if H value is not the same for both points:
                            make sure V value of either point is not ver_inside
                    or V value is the same
                    or  if V value is not the same for both points:
                            make sure H value of either point is not hor_inside
                This cutting across has edge cases that are not included here
                but for this problem where lines are horizontal or vertical it's all good.


I am missing a part here - where I should keep track of inside vs outside. 
at least one point of the rectangle should be inside the curve.

'''
class Point:
    def __init__(self,x=None,y=None,H=None, V=None):
        self.x=x #coordinate
        self.y=y #coordinate
        self.H=H #relative position to another object.
        self.V=V #relative position to another object.
        # H: -1 = west, 0 = inside, 1= east
        # V:-1 = below, 0= inside, 1=above

def sign(x):
    return int(x>0)-int(x<0)    

# def get_side(p,rect):
#     bottom,right,top,left=rect
#     p.H=sign(sign(p.x-left)+sign(p.x))
#     p.V=sign(sign(p.y-bottom)+sign(p.y-top))

#     side=''
#     if p.V==1:
#         side+='N'
#     if p.V==-1:
#         side+='S'
#     if p.H==1:
#         side+='E'
#     if p.H==-1:
#         side+='W'
#     return side

#without the boundary. if the boundaries touch - it will return false. 
def contains(b, rect):
    bottom,right,top,left=rect

    # S=False
    # SE=False
    # NE=False
    # N=False
    # NW=False
    # W=False
    # SW=False


    for i in range(len(b)+1):
        curr_p=b[i%len(b)]
        next_p=b[(i+1)%(len(b))]

        curr_p.H=sign(sign(curr_p.x-left)+sign(curr_p.x))
        curr_p.V=sign(sign(curr_p.y-bottom)+sign(curr_p.y-top))
        next_p.H=sign(sign(next_p.x-left)+sign(next_p.x))
        next_p.V=sign(sign(next_p.y-bottom)+sign(next_p.y-top))

        b_contains_rect=True #innocent until proven guilty.

        #check that boundary is on all sides of the rectangle.


        #check if points are inside
        if curr_p.H==0 and curr_p.V==0:
            b_contains_rect=False
        if next_p.H==0 and next_p.V==0:
            b_contains_rect=False

        if curr_p.H != next_p.H:
            if curr_p.V == 0 or next_p.V==0:
                b_contains_rect=False
        if curr_p.V != next_p.V:
            if curr_p.H == 0 or next_p.V==0:
                b_contains_rect=False

        if b_contains_rect==False:
            break

    # if not (got_south and got_east and got_north and got_west):
        # b_contains_rect=False

    return b_contains_rect

#get rekd, yo!
def get_rect(point1, point2,shrink=False):
    x1,y1=point1.x, point1.y
    x2,y2=point2.x, point2.y
    
    bottom=min(y1,y2)
    top=max(y1,y2)+1
    left=min(x1,x2)
    right=max(x1,x2)+1

    if shrink:
        bottom+=1
        top-=1
        left+=1
        right-=1

    return bottom, right, top, left

#calculate the rectangle area, leftover from part 1
def get_area(point1, point2):
    x1,y1=point1.x, point1.y
    x2,y2=point2.x, point2.y
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
    
    boundary=[]
    for i in range(N):
        p=Point(x=X[i],y=Y[i])
        boundary.append(p)
    for i in range(N):
        print(boundary[i].x, boundary[i].y)



    all_areas=np.zeros((N,N))
    final_area=0
    for i in range(N):
        for j in range(i+1,N):
            p1=boundary[i]
            p2=boundary[j]

            area=get_area(p1,p2)
            
            rect=get_rect(p1,p2,shrink=True)
            
            if contains(boundary, rect):
                all_areas[i,j]=area
                print(f'valid rect at points: {p1.x},{p1.y} and {p2.x},{p2.y}')
                if area>final_area:
                    final_area=area
                    print(f'largest area so far at points = {p1.x},{p1.y} and {p2.x},{p2.y}')

    print('-'*30)
    print(final_area)
    print('-'*30)
    plt.plot(X,Y,'r.-')
    plt.show()
    plt.matshow(all_areas)
    plt.show()