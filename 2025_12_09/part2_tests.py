import sys
import numpy as np
import matplotlib.pylab as plt

def sign(x):
    return int(x>0) - int(x<0)

def get_direction(curr_point, next_point):
    return (
        sign(next_point[0]-curr_point[0]), 
        sign(next_point[1]-curr_point[1])
    )

def get_angle(curr_point, next_point, next_next_point):
    dir1=get_direction(curr_point,next_point)
    dir2=get_direction(next_point,next_next_point)

    rot_ccw=np.array([[0,-1],[1,0]])

    if np.all((rot_ccw@np.array(dir1).T) == dir2 ):
        # print('counter cw')
        return 1
    elif np.all(((-rot_ccw)@np.array(dir1).T) == dir2 ):
        # print('clockwise')
        return -1
    else:
        print('not a correct 90 degree rotation')
        return None


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

    # plt.ion()
    # fig,ax=plt.subplots(figsize=(8,6))
    # data0,=ax.plot(X+0.5,Y+0.5,'r.-',linewidth=0.5)
    # pt1,=ax.plot([],[],'bo')
    # pt2,=ax.plot([],[],'bv')
    # pt3,=ax.plot([],[],'go')

    # ax.set_xlim(0,max(X)+2)
    # ax.set_ylim(0,max(Y)+2)
    # # ax.set_xticks(np.arange(0,max(X)+2))
    # # ax.set_yticks(np.arange(0,max(Y)+2))
    # plt.grid(True)

    total_angle=0
    all_angles=[]
    for i in range(N):
        if i==N-1:
            next_point=(X[0],Y[0])
            next_next_point=(X[1],Y[1])
        elif i==N-2:
            next_point=(X[i+1],Y[i+1])
            next_next_point=(X[0],Y[0])
        else:
            next_point=(X[i+1],Y[i+1])
            next_next_point=(X[i+2],Y[i+2])
        curr_point=(X[i],Y[i])

        #for debugging
        # pt1.set_data([X[i]+0.5],[Y[i]+0.5])
        # pt2.set_data([next_point[0]+0.5],[next_point[1]+0.5])
        # pt3.set_data([next_next_point[0]+0.5],[next_next_point[1]+0.5])
        angle=get_angle(curr_point,next_point,next_next_point)
        total_angle+=angle
        all_angles.append(total_angle)
        # plt.title(f'angle = {angle}, total angle so far {total_angle}')
        # plt.pause(0.005)
        # fig.waitforbuttonpress()
    print('done with the loop')
    print(total_angle)


    # plt.ioff() # Turn off interactive mode at the end
    # plt.show() # Keep the final plot window ope


    plt.figure()
    plt.plot(X,Y,'r-')
    plt.show()


    plt.figure()
    plt.plot(all_angles)
    plt.show()
    