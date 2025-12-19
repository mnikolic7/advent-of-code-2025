import sys
import numpy as np
from scipy.signal import convolve
import matplotlib.pylab as plt

# define a function for readability:
def getRolls(grid):
    kernel=np.ones((3,3), dtype=np.uint8) # kernel of ones. 

    neighbors=convolve(grid, kernel, mode='same') #convolve with the kernel (sum neighborhoods)
    neighbors=(neighbors < 5)*grid # reachable rolls
    grid=grid-neighbors #update the grid by removing reachable rolls.
    return grid 

#solution to part 2 of puzzle from Dec 4, 2025
if __name__ == "__main__":
    fname=sys.argv[1]

    lines=[]
    with open(fname, 'r') as f:
        for line in f:
            lines.append(line.strip())

    grid=np.array([list(line) for line in lines])
    grid=(grid=='@').astype('uint8')

    # run at least once
    prev_grid=grid.copy()
    final_grid=getRolls(prev_grid)

    #do some plotting to watch as things go, to make sure there are no bugs.
    plt.ion()
    fig, axes=plt.subplots(1,3, figsize=(12,4))
    im1=axes[0].imshow(prev_grid)
    fig.colorbar(im1, ax=axes[0])
    axes[0].set_title('Prev.')

    im2=axes[1].imshow(final_grid)
    fig.colorbar(im2, ax=axes[1])
    axes[1].set_title('Current')

    im3=axes[2].imshow(prev_grid-final_grid)
    fig.colorbar(im3, ax=axes[2])
    axes[2].set_title('diff')

    while np.any(prev_grid-final_grid): #check that final grid is different from prev_grid.
        prev_grid=final_grid.copy()
        final_grid=getRolls(prev_grid)

        im1.set_data(prev_grid)
        im2.set_data(final_grid)
        im3.set_data(prev_grid-final_grid)
        plt.pause(0.05)
    
    plt.ioff()
    plt.show()

    print(np.sum(grid-final_grid))
