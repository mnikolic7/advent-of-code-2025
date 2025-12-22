import sys
import math

#solution to part 1 of puzzle from Dec 6, 2025
if __name__ == "__main__":
    fname=sys.argv[1]

    lines=[]
    with open(fname, 'r') as f:
        for line in f:
            l=line.strip().split() #split without argument removes all whitespace, and returns just values.
            lines.append(l)

    Nrows=len(lines)
    Ncols=len(lines[0]) #ideally we should check that str.split() did the right thing up there
    #but it works, so I won't complicate the things here.
    final_result=0
    for i in range(Ncols):
        curr_numbers=[]
        for j in range(Nrows-1):
            curr_numbers.append(int(lines[j][i]))

        sum_or_product=lines[Nrows-1][i]

        if sum_or_product=='+':
            curr_result=sum(curr_numbers)
        elif sum_or_product=='*':
            curr_result=math.prod(curr_numbers)

        final_result+=curr_result

    print(final_result)