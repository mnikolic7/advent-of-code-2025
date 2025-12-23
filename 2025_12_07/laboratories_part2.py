import sys
import numpy as np
import matplotlib.pylab as plt

#solution to part 2 of puzzle from Dec 7, 2025
if __name__ == "__main__":
    fname=sys.argv[1]

    lines=[]
    with open(fname, 'r') as f:
        for line in f:
            lines.append(line.strip())

    #not the most memory-elegant, but it's ok for this puzzle.
    grid=np.array([list(line) for line in lines])
    manifold=(grid=='S').astype('uint64') #now zeros except at S, will be updated.
    #overflow is a serious problem in this.
    #max manifold value (number of ways to arrive at a point) reached values > 2^45 
    #total sum was larger than 2^48 so uint64 is the only that works. 
    #numpy was worried about it so when I summed it it gave me a float64 back. Fortunately it was only 49 bits needed...

    splitters=(grid=='^').astype('uint8')

    #see the tachyon tannenbaum 
    plotON=True
    plot_bits=True #see how many bits you need to store the number of timelines at each position.

    if plotON:
        #illustrate the progress. Show the tachyon tannenbaum :)
        plt.ion()
        fig, axes=plt.subplots(1,2, figsize=(10,4))
        if plot_bits:
            im1=axes[0].matshow(np.log2(manifold+0.1), vmin=-1,vmax=0)
            fig.colorbar(im1, ax=axes[0])
            axes[0].set_title('Bits to store beam paths')
        else:
            im1=axes[0].matshow(manifold)
            fig.colorbar(im1, ax=axes[0])
            axes[0].set_title('Beam paths')

        im2=axes[1].matshow(splitters, vmin=0, vmax=2)
        fig.colorbar(im2, ax=axes[1])
        axes[1].set_title('Splits')

        axes[0].set_xticks([])
        axes[0].set_yticks([])
        axes[1].set_xticks([])
        axes[1].set_yticks([])

    Nr,Nc=manifold.shape

    # print(manifold[0])
    for row in range(1,Nr):
        for col in range(Nc):
            # curr_value=manifold[row][col]
            value_above=manifold[row-1][col]
            if value_above==0:
                continue
                #if value above is zero, don't change anything. no input beam.
                #this should also take care of the boundary errors for this puzzle. 
            
            #reach here only if there is an input beam.
            if splitters[row][col]==0: #if we are not at a splitter, propagat the beam simply
                manifold[row][col]+=value_above
            elif splitters[row][col]>0: #we are at a splitter
                manifold[row][col-1]+=value_above 
                manifold[row][col+1]+=value_above #always += increment.

                #col+1 and col-1 are unsafe, but the input should not contain those cases. 
                #maybe I will add a safe handling later.
            else: 
                raise ValueError('you should not reach line 48.')
        # print(manifold[row])


        hits=splitters[row]*(manifold[row-1]>0) #it will ignore unhit splits
        splitters[row]+=hits #label splitters that were hit by a beam with 2. otherwise 1.
        if plotON:
            if plot_bits:
                im1.set_data(np.log2(manifold+0.1))
                im1.set_clim(vmin=-1, vmax=np.log2(manifold.max()))
            else:
                im1.set_data(manifold)
                im1.set_clim(vmin=manifold.min(), vmax=manifold.max())
            im2.set_data(splitters)
            # im2.set_clim(vmin=splitters.min(), vmax=splitters.max())
            plt.pause(0.001)
    

    if plotON:
        plt.ioff()
        plt.show()

    print('-'*50)
    print(sum(manifold[len(manifold)-1]))
    print(max(manifold[len(manifold)-1]))
    print('-'*50)