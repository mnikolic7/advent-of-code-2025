import sys
import numpy as np
import matplotlib.pylab as plt

def split_beams(hit_locations):
    new_beams=np.zeros_like(hit_locations)
    for i in range(len(hit_locations)):
        if hit_locations[i]==1:
            #handle some edge cases (which don't really happen)
            if hit_locations[i]==len(hit_locations):
                new_beams[i-1]+=1
            elif hit_locations[i]==0:
                new_beams[i+1]+=1
            else:
                new_beams[i-1]+=1
                new_beams[i+1]+=1
    return new_beams

#solution to part 2 of puzzle from Dec 7, 2025
if __name__ == "__main__":
    fname=sys.argv[1]

    lines=[]
    with open(fname, 'r') as f:
        for line in f:
            lines.append(line.strip())

    #not the most memory-elegant, but it's ok for this puzzle.
    grid=np.array([list(line) for line in lines])
    beams=(grid=='S').astype('uint8') #will be updated.
    splitters=(grid=='^').astype('uint8')
    paths=beams.copy()

    Nlevels=len(grid)
    
    plt.ion()
    fig, axes=plt.subplots(1,3, figsize=(12,4))
    im1=axes[0].matshow(beams)
    fig.colorbar(im1, ax=axes[0])
    axes[0].set_title('Beams')

    im2=axes[1].matshow(splitters, vmax=2)
    fig.colorbar(im2, ax=axes[1])
    axes[1].set_title('Splits')

    im3=axes[2].matshow(paths)
    fig.colorbar(im3, ax=axes[2])
    axes[2].set_title('Paths')

    for i in range(1,len(beams)):
        input_beams=beams[i-1] #prev_line or input_beams

        #splits
        hits=splitters[i]*(input_beams>0) #it will ignore unhit splits
        splitters[i]+=hits #label splitters that were hit by a beam with 2. otherwise 1.

        #expand beams hit splits
        new_beams=split_beams(hits)
        
        total_curr_beams=new_beams+input_beams-hits #each hit adds new beams, but removes one for each hit.
        beams[i]=total_curr_beams
        total_curr_paths=total_curr_beams.copy()

        paths[i]=total_curr_paths

        im1.set_data(beams)
        im1.set_clim(vmin=beams.min(), vmax=beams.max())
        im2.set_data(splitters)
        im2.set_clim(vmin=splitters.min(), vmax=splitters.max())
        im3.set_data(paths)
        im3.set_clim(vmin=paths.min(), vmax=paths.max())
        plt.pause(0.01)
    
    plt.ioff()
    plt.show()


    print(sum(paths[len(paths)-1]))

