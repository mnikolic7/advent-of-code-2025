import numpy as np
import pandas as pd
import sys

#solution to part 1 of puzzle from Dec 1, 2025
if __name__ == "__main__":
	fname=sys.argv[1]

	df=pd.read_csv(fname, sep=r"\s+", header=None, names=["turns"])

	position=50
	count_of_zeros=0

	for item in df['turns']:
		if item[0] == 'R':
			direction=1
		elif item[0] == 'L':
			direction=-1
		else:
			direction=0
			print('WARNING! No direction given')

		
		steps=int(item[1:])
		position=position+(direction*steps)
		#don't be fancy, just be simple
		#I always get one-off errors when I use mod, so better don't risk it 
		while position>99:
			position=position-100 
		while position<0:
			position=position+100
		if position==0:
			count_of_zeros+=1

	print('final result: ',count_of_zeros)