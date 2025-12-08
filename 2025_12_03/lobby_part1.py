import sys

#solution to part 1 of puzzle from Dec 3, 2025
if __name__ == "__main__":
    fname=sys.argv[1]

    lines=[]
    with open(fname, 'r') as f:
        for line in f:
            lines.append(line.strip())
    
    joltages=[]
    for line in lines:
        battery=[int(x) for x in list(line)]
        # print(battery)
        max1=max(battery)
        idx1=battery.index(max1)
        # print(f'max {max1} at {idx1}, battery length {len(battery)}')
        if idx1==len(battery)-1: #this is the weird case when we found max as the last digit. So this must be the second digit. 
            max2=max(battery[:idx1])
            joltage=int(str(max2)+str(max1))
        else: #this is the default case when we found the max anywhere but last. so it must be the first digit.
            max2=max(battery[idx1+1:])
            joltage=int(str(max1)+str(max2))
        joltages.append(joltage)

    print(joltages)
    print('-'*50)
    print('sum =', sum(joltages))
    print('-'*50)