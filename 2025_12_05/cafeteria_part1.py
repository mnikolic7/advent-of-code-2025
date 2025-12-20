import sys


#simple, very simple solution:

#check if number n is in any of the ranges
def isFresh(n, ranges):
    inRange=False
    i=0
    while (not inRange) and ( i<len(ranges) ):
        if n>=ranges[i][0] and n<=ranges[i][1]:
            inRange=True
            print(f'ingredient {n} is fresh.')
        i+=1
    return inRange

#solution to part 1 of puzzle from Dec 5, 2025
if __name__ == "__main__":
    fname=sys.argv[1]

    fresh_ranges=[]
    ingredients=[]
    getIngredientsNow=False
    with open(fname, 'r') as f:
        for line in f:
            if not line.strip():
                getIngredientsNow=True
                continue
            if getIngredientsNow:
                ingredients.append(int(line.strip()))
            else:
                fresh_ranges.append(list( map(int, line.strip().split('-')) ) )

    print(ingredients)

    print('-'*10)
    print(fresh_ranges)
    #there are around ~1000 ingredients in my input
    #and about ~180 ranges. All we need to check is if an ingredient falls within any of the ranges.
    #I will just check ingredients one by one. 

    #straightforward solution. 
    count=0
    for ingredient in ingredients:
        if isFresh(ingredient, fresh_ranges):
            count+=1

    print(f'Total count is {count}.')