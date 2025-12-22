import sys
import numpy as np
# from scipy.signal import convolve

def split_hits(hit_locations):
    split_locations=np.zeros_like(hit_locations)
    for i in range(len(hit_locations)):
        if hit_locations[i]==1:
            #handle some edge cases (which probably don't happen)
            if hit_locations[i]==len(hit_locations):
                split_locations[i-1]=1
            elif hit_locations[i]==0:
                split_locations[i+1]=1
                split_locations[i]=0
            else:
                split_locations[i-1]=1
                split_locations[i+1]=1
    #unexpected results will be returned for two splitters right next to each other.
    #I assume that doesn't happen.
    return split_locations

#solution to part 1 of puzzle from Dec 7, 2025
#I will base this on the 12/04 solution. I have a feeling it may be handy.
if __name__ == "__main__":
    fname=sys.argv[1]

    lines=[]
    with open(fname, 'r') as f:
        for line in f:
            lines.append(line.strip())

    #not the most memory-elegant, but it's ok for this puzzle.
    grid=np.array([list(line) for line in lines])
    manifold=(grid=='S').astype('uint8') #will be updated.
    splitters=(grid=='^').astype('uint8')


    #just propagate the tachyons.
    #until i, it's representing beams,
    #at i and later, it is representing splitters. It's weird sorry.
    print(manifold[0])
    split_counter=0
    for i in range(1,len(manifold)):
        prev_line=manifold[i-1] #prev_line or input_beams

        #splits
        hits=splitters[i]*prev_line #it will ignore unhit splits
        split_counter+=sum(hits)
        #expand beams hit splits
        splitted=split_hits(hits) #abusing english grammar to remove coding ambiguity.

        curr_line=prev_line-hits+splitted
        manifold[i]=curr_line>0
        print(manifold[i])

    print(split_counter)



