import sys
import numpy as np
import matplotlib.pylab as plt


#define a Beam class for the "graph" in which each beam is a node
#each beam has a start and the end level (from a splitter to a splitter)
#and it has a list of parents and children.
#finally it has a value n - which is the value of how many ways we can enter 
#the beam it is equal to the sum of parent.n for parent in parents.
#more for my own practice. 
class Beam:
    def __init__(self):
        self.pos=None #horizontal position in the graph.
        self.start=None #vertical start position
        self.end=None #vertical end position
        self.n=None #number of ways to start in this graph
        self.parents=[] #parent beams
        self.children=[] #children beams.

    def add_child(self, child: "Beam"):
        if child is self:
            raise ValueError("Cannot add self as child")
        if child not in self.children:
            self.children.append(child)
        if self not in child.parents:
            child.parents.append(self)

    def add_parent(self, parent: "Beam"):
        if parent is self:
            raise ValueError("Cannot add self as parent")
        if parent not in self.parents:
            self.parents.append(parent)
        if self not in parent.children:
            parent.children.append(self)

    def __str__(self):
        return (f"Beam instance at pos={self.pos}. s={self.start}, e={self.end}, n={self.n}\n"
                f"with {len(self.parents)} parents, and {len(self.children)} children.")


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

#solution to part 2 of puzzle from Dec 7, 2025
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

    #just propagate the tachyons. From part 1
    #until i, it's representing beams,
    #at i and later, it is representing splitters. It's weird sorry.

    # ok so the next code block is indeed weird. so I will have to rewrite it.
    #in fact I need to rewrite the construction of the graph now with the Beam class. 
    #where beams are nodes, and splitters are edges connecting beams. 

    #then it should be quite easy to write a recursion with memoization since the Beam objects 
    #will have n=None or something valid. So it's going to be a fun easy recursion. 
    #but the way I wrote this for loop really prevented me from solving this...typical aoc
    #part one can be done easily if you cut corners, but part 2 can't. 

    print(manifold[0])
    for i in range(1,len(manifold)):
        prev_line=manifold[i-1] #prev_line or input_beams

        #splits
        hits=splitters[i]*prev_line #it will ignore unhit splits
        #expand beams hit splits
        splitted=split_hits(hits) #abusing english grammar to remove coding ambiguity.

        curr_line=prev_line-hits+splitted
        manifold[i]=curr_line>0
        print(manifold[i])

    #test beam class.
    x=Beam()
    x.pos=1
    x.n=10
    x.start=0
    x.end=1
    print(x)
    ###############leftover code below. some useful plotting stuff there. 
    
    # plt.ion()
    # fig, axes=plt.subplots(1,3, figsize=(12,4))
    # im1=axes[0].matshow(beams)
    # fig.colorbar(im1, ax=axes[0])
    # axes[0].set_title('Beams')

    # im2=axes[1].matshow(splitters, vmax=2)
    # fig.colorbar(im2, ax=axes[1])
    # axes[1].set_title('Splits')

    # im3=axes[2].matshow(paths)
    # fig.colorbar(im3, ax=axes[2])
    # axes[2].set_title('Paths')

    # print(beams[0])
    # for i in range(1,len(beams)):
    #     input_beams=beams[i-1] #prev_line or input_beams

    #     #splits
    #     hits=splitters[i]*(input_beams>0) #it will ignore unhit splits
    #     splitters[i]+=hits #label splitters that were hit by a beam with 2. otherwise 1.

    #     #expand beams hit splits
    #     new_beams=split_beams(hits)
        
    #     total_curr_beams=new_beams+input_beams-hits #each hit adds new beams, but removes one for each hit.
    #     beams[i]=total_curr_beams
    #     total_curr_paths=total_curr_beams.copy()
    #     print(beams[i])
    #     paths[i]=total_curr_paths

    #     im1.set_data(beams)
    #     im1.set_clim(vmin=beams.min(), vmax=beams.max())
    #     im2.set_data(splitters)
    #     im2.set_clim(vmin=splitters.min(), vmax=splitters.max())
    #     im3.set_data(paths)
    #     im3.set_clim(vmin=paths.min(), vmax=paths.max())
    #     plt.pause(0.01)
    
    # plt.ioff()
    # plt.show()


    # print(sum(paths[len(paths)-1]))

