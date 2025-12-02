import numpy as np
import pandas as pd
import sys

#solution to part 2 of puzzle from Dec 1, 2025
if __name__ == "__main__":
	fname=sys.argv[1]

	df=pd.read_csv(fname, sep=r"\s+", header=None, names=["turns"])

	position=50
	count_of_zeros=0
	i=0
	for item in df['turns']:
		if item[0] == 'R':
			direction=1
		elif item[0] == 'L':
			direction=-1
		else:
			direction=0
			print('WARNING! No direction given')


		steps=int(item[1:])
		assert(steps!=0)
		
		full_turns=steps//100
		steps=steps-full_turns*100 #just the remainder over hundred steps.

		new_position=(position+direction*steps)
		
		count_of_zeros+=full_turns
		# ok trying to be clever. I used the pen and paper to figure the edge cases out:
		# if going right you can get a result between:
		#     2 and 99 (without going over zero), and 100 and 198 (with going over zero)
		#if going left you can get a result between:
		#     1, 98 (without going over zero), and -98 and 0 (with going over zero, zero inclusive)
		#but there is an important caveat: if you started at zero you could get anything between -1 and -99,
		#so we must nest a double condition in the if statement. this really was a puzzle. :) 

		if new_position>=100:
			count_of_zeros+=1
		elif new_position==0:
			count_of_zeros+=1
		elif new_position<0 and position!=0:
			count_of_zeros+=1

		# calculate using mod, don't be scared.
		position=(new_position)%100
		i+=1
		print('idx ', i, 'position: ', position,': ft=',full_turns, 'new_pos: ', new_position, ' count=',count_of_zeros)
	print('final result: ',count_of_zeros)