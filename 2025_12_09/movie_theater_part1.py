import sys
import matplotlib.pylab as plt
import matplotlib.patches as patches

#a bit of a clever way to calculate the rectangle area
def getArea(point1, point2):
    x1,y1=point1
    x2,y2=point2
    #bottom left
    x_BL,y_BL=(min(x1,x2),min(y1,y2))
    #top right
    x_TR, y_TR=(max(x1,x2),max(y1,y2))
    x_TR+=1 #tiles are integers, so count correctly.
    y_TR+=1
    return (y_TR-y_BL)*(x_TR-x_BL)

def plotRect(point1,point2):
    x1,y1=point1
    x2,y2=point2
    fig, ax = plt.subplots()
    plt.plot(x1,y1,'ro',x2,y2,'r+')
    #make sure that you take x1,y1 is the bottom-left corner.

    #going counterclockwise around the rectangle from bottom left.
    x_a,y_a=(min(x1,x2),min(y1,y2))
    x_b,y_b=(max(x1,x2),min(y1,y2))
    x_c,y_c=(max(x1,x2),max(y1,y2))
    x_d,y_d=(min(x1,x2),max(y1,y2))

    plt.plot(x_a,y_a,'k.')
    plt.plot(x_b,y_b,'k.')
    plt.plot(x_c,y_c,'k.')
    plt.plot(x_d,y_d,'k.')

    y2=y2+1
    x2=x2+1
    area=(y_c+1-y_a)*(x_c+1-x_a)
    plt.title(f'area = {area}')
    rect=patches.Rectangle((x_a,y_a),x_c-x_a,y_c-y_a,alpha=0.5)
    ax.add_patch(rect)
    plt.show()
    return area

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
    final_area=0
    #just do a simple N*(N-1)/2 solution.
    for i in range(N):
        for j in range(i+1,N):
            point1=(x_list[i],y_list[i])
            point2=(x_list[j],y_list[j])
            area=getArea(point1,point2)
            print(area)
            print('-----')
            if area > final_area:
                final_area=area
    print(f'max area={final_area}')