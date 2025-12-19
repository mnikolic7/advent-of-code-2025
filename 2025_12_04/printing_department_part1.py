import sys
import numpy as np
from scipy.signal import convolve

#solution to part 1 of puzzle from Dec 4, 2025
if __name__ == "__main__":
    fname=sys.argv[1]

    lines=[]
    with open(fname, 'r') as f:
        for line in f:
            lines.append(line.strip())

    grid=np.array([list(line) for line in lines])
    grid=(grid=='@').astype('uint8')

    kernel=np.ones((3,3), dtype=np.uint8) # kernel of ones. 

    neighbors=convolve(grid, kernel, mode='same') #convolve with the kernel (sum neighborhoods)
    neighbors=(neighbors < 5)*grid # return reachable 

    print(np.sum(neighbors.ravel()))

