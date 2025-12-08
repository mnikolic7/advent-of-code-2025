import sys

def max_joltage(battery: list[int], M=12) -> int:
    joltage=''

    M=M-1 #M is now the number of remaining switches to lfip.

    start_idx=0
    end_idx=len(battery)-M #as long as there are enough numbers behind the max, keep searching for the max

    print('battery is: ', battery)
    while M>=0:
        subsection=battery[start_idx:end_idx]

        ##debugging prints. best to pipe this to a file if debugging
        '''
        print('searching in: ', battery[start_idx:end_idx])
        idx_list=[]
        for x in range(len(battery)):
            idx_list.append((len(battery)-x)%10)
        print('searchin idx: ', idx_list)
        x=[0]*len(battery)
        x[start_idx:end_idx]=[1]*(end_idx-start_idx)
        print('search indic: ', x)
        print('searching in: ', battery)
        '''
        ##

        m=max(subsection)
        start_idx=subsection.index(m)+1+start_idx
        
        joltage+=str(m)
        
        M-=1
        end_idx=len(battery)-M
        
        #print(f'max is {m}, new start is {start_idx}, new_end is {end_idx}, remaining {M} out of 12')
    #print('---')
    return int(joltage)

#well I have to fix it. it doesn't quite work.

#solution to part 2 of puzzle from Dec 3, 2025
if __name__ == "__main__":
    fname=sys.argv[1]

    lines=[]
    with open(fname, 'r') as f:
        for line in f:
            lines.append(line.strip())
    
    joltages=[]
    for line in lines:
        battery=[int(x) for x in list(line)]
        curr_max_joltage=max_joltage(battery)
        joltages.append(curr_max_joltage)
        print(f'curr max joltage is {curr_max_joltage}')
        print('-'*50)

    print(joltages)
    print('-'*50)
    print('sum =', sum(joltages))
    print('-'*50)