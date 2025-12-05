import sys
from itertools import product # turns out I need some combinations to make this generally work well.

"""
dec 02, 2025 - puzzle part 2 solution.
simplify and use brute force. 
all you need is to write a function that check individual one, and then check all numbers in the input.
the input goes easy and doesn't have that many numbers to run. 

so the straightforward solution is still one line, except that we need to make isInvalid function 
which is slighly more complicated. 
it will:
1. take an id.
2. find all of the divisors of len(id). max len id is 11, I will not hardwire this only beceause I want to remind myself how to do it. 
3. check if it is repeated for each divisor. 
"""

#interesting thing here is that each divisor comes in pair:
#i.e. for 12, we check 2 (we automatically get 6)
#             we check 3 (we automatically get 4)
# at worst it is a square and for 25 we check 5 and get 5, so it's more 
#efficient to just check up to sqrt(N)
def getDivisors(N):
	i=2 #we don't care about 1 (but we care about N) for our application
	# it is good that they are sorted in ascending order.
	#that's how the problem statement does it.
	divisors=[]
	while i**2 <= N:
		if N%i==0:
			divisors.append(i)
		i+=1

	# #add the second half of divisors.

	#### this is of course wrong, because python's iterables are nice and efficient.
	# I am leaving it here as a lesson for myself. I learned how to do this better. 
	######start WRONG
	# for d in divisors:
	# 	divisors.append((N//d))

	# and ths is another wrong way:
	#divisors.extend( N//d for d in divisors) #same problem. infinite loop
	######end WRONG

	#and this is the correct python way:
	for d in divisors[:]: #shallow copy
		if N//d==d: # remove squares (double entries):
			continue
		else:
			divisors.append(N//d)

	divisors.append(N)
	# I checked that the divisors are unique. 
	return divisors

def isInvalid(int_number):
	str_number=str(int_number)
	N=len(str_number)

	#I forgout about single digit numbers. I actually never ran this, 
	#and simply subtracted 45(sum(1-9)) from my result and IT WORKED!  
	if N==1:
		return False

	divisors=getDivisors(N)
	# print(f'{N} is divisible by {divisors}')

	#d is divisor of N
	for d in divisors:
		#split string into d parts
		substrings=[]
		step=N//d
		for j in range(0,N,step):
			substrings.append(str_number[j:j+step])
		#check that they are all the same
		all_same=all( s == substrings[0] for s in substrings )
		#if same return true
		if all_same:
			return True
		#else try the next divisor
	#if you can't find any
	return False

def get_invalid_IDs(start, end):
	return [x for x in range(start, end+1) if isInvalid(x)] #this is python fun one line solution

#solution to part 2 of puzzle from Dec 2, 2025
if __name__ == "__main__":
	fname=sys.argv[1]

	with open(fname, 'r') as f:
		line = f.readline().strip()

	ranges=line.split(',')

	invalid_IDs=[]
	for r in ranges:
		s,e=r.split('-')
		curr_invalidIDs = get_invalid_IDs(int(s),int(e))
		invalid_IDs+=curr_invalidIDs

	#show yourself your calculation - it helps. 
	print('-'*50)
	print('invalid IDs:')
	print(invalid_IDs)
	print('-'*50)
	print('Sum:')
	print(sum(invalid_IDs))
	print('-'*50)
	
