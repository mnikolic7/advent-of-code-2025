import sys

#solution to part 2 of puzzle from Dec 5, 2025
if __name__ == "__main__":
    fname=sys.argv[1]

    starts=[]
    ends=[]
    with open(fname, 'r') as f:
        for line in f:
            if not line.strip():
                getIngredientsNow=True
                break
            l=line.strip().split('-')
            starts.append(int(l[0]))
            ends.append(int(l[1]))

    #I checked on the subreddit for some hints- unfortunately this spoiled a part of it for me, but I was very close.
    #At least I now know how to solve this problem and I implement. I didn't look at any code. 
    #implementation is all mine. 

    edges=starts+ends #concatenate
    indicator=[1]*len(starts)+[-1]*len(ends)


    idx=sorted(range(len(edges)), key=edges.__getitem__)
    # print(idx)

    edges=[edges[i] for i in idx]
    indicator=[indicator[i] for i in idx]

    new_starts=[]
    new_ends=[]

    intervalCounter=0
    for e,i in zip(edges, indicator):
        if intervalCounter==0 and i==1:
            new_starts.append(e)

        if intervalCounter==1 and i==-1:
            new_ends.append(e)

        intervalCounter+=i

    final_count=0
    for s,e in zip(new_starts,new_ends):
        final_count+=e+1-s

    print(final_count)