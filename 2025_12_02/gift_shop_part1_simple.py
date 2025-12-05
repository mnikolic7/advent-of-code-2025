import sys

#dec 02, 2025 - puzzle part 1 solution.
#simplify and use brute force. 

#I checked Mate's code - which was fun to look at because its object oriented as hell.
#but it just confirmed to me that I should take the simple approach.
def isMirrored(int_number):
	str_number=str(int_number)
	N=len(str_number)
	if (N%2==1):
		return False

	if str_number[:N//2] == str_number[N//2:]:
		return True
	else:
		return False

def get_invalid_IDs(start, end):
	return [x for x in range(start, end+1) if isMirrored(x)] #this is python fun.

#solution to part 1 of puzzle from Dec 2, 2025
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

	print('-'*50)
	print('invalid IDs:')
	print(invalid_IDs)
	print('-'*50)
	print('Sum:')
	print(sum(invalid_IDs))
	print('-'*50)
	
