import sys
import math
import numpy as np

#solution to part 2 of puzzle from Dec 6, 2025
#ok this was a proper programming assignment.
if __name__ == "__main__":
    fname=sys.argv[1]

    lines=[]
    with open(fname, 'r') as f:
        for line in f:
            lines.append(line)

    Nrows=len(lines)
    #well, the sign + or * is at the very beginning of the section for each line, so I will just use that as the length.
    sum_or_product=lines[Nrows-1]
    sidx=[] #sidx is subsection start index.
    for i in range(len(sum_or_product)):
        if sum_or_product[i]=='+' or sum_or_product[i]=='*':
            sidx.append(i)

    Ncols=len(lines[0])

    sidx.append(Ncols)
    #but Nproblems is some other number.
    Nproblems=len(sidx)
    #then construct the matrix:

    #solve problems one by one. the order doesn't matter.
    final_result=0

    for n in range(1,Nproblems):
        curr_start=sidx[n-1]
        curr_end=sidx[n]-1 #account for space at the end.
        print('---current problem---')
        curr_matrix=[]
        for r in range(Nrows-1):
            curr_matrix.append(lines[r][curr_start:curr_end])

        #transpose the matrix. This will ensure the numbers are added the cephalopod way.
        #this relies on the fact that the order of summation or product doesn't matter.
        #just that the vertical values are included correctly.
        curr_matrix=[list(row) for row in zip(*curr_matrix)]

        curr_numbers=[]
        for row in curr_matrix:
            curr_numbers.append(int(''.join(row)))

        print(curr_numbers)
        
        if sum_or_product[sidx[n-1]]=='*':
            curr_result=math.prod(curr_numbers)
        elif sum_or_product[sidx[n-1]]=='+':
            curr_result=sum(curr_numbers)
        else:
            print('you should not reach line 56')
        print(f'curr result={curr_result}')
        final_result+=curr_result

    print(final_result)




