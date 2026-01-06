import sys
import numpy as np
import sympy as sp

#linear algebra practice. 
#I should just practice SVD here to solve the equation.
#let me start with libraries, as that is more practical.

if __name__=="__main__":
	fname=sys.argv[1]

	LIGHTS=[]
	BUTTONS=[]
	JOLTAGES=[]
	with open(fname) as file:
		for line in file:
			l=line.strip().split()
			lights=l[0][1:-1] #first item, get rid of bracket characters
			joltages=l[-1][1:-1] #last item, get rid of curly brackets
			buttons=l[1:-1] #items in between

			#get switches in binary-ready.
			binary=''
			for c in lights:
				if c=='#':
					binary+='1'
				else:
					binary+='0'
			LIGHTS.append(binary)

			#get joltages as integers.
			JOLTAGES.append([int(j) for j in joltages.split(',')])

			butts=[]
			for butt in buttons:
				butt=butt[1:-1].split(',')
				butt=[int(b) for b in butt]
				butts.append(butt)
			BUTTONS.append(butts)

	INF=float('inf')

	#inspect data: there are overdetermined and underdetermined 
	#equations
	# for IDX in range(len(JOLTAGES)):
	# 	print(f'Joltage length: {len(JOLTAGES[IDX])}')
	# 	print(f'buttons length: {len(BUTTONS[IDX])}')
	# 	print('-----')
	
	#inspect data more. 
	#everything is so singular as heck.
	# IDX=0
	# n_nonsingular=0
	# for IDX in range(len(JOLTAGES)):
	# 	joltages=JOLTAGES[IDX]
	# 	button_list=BUTTONS[IDX]

	# 	M=len(joltages)
	# 	N=len(button_list)

	# 	X=np.zeros((M,N)) #m by n matrix such that
	# 	y=np.zeros((M,1))
	# 	#the equation is :
	# 	# X*b=y, where dim(X)=m x n, b=n x 1 and y=m x 1
	# 	for i in range(N):
	# 		button=button_list[i]
	# 		for b in button:
	# 			X[b,i]+=1

	# 	for i,j in enumerate(joltages):
	# 		y[i]=j

	# 	det_inner=np.linalg.det(X.T@X)
	# 	det_outer=np.linalg.det(X@X.T)
	# 	if np.abs(det_inner) > 0.01 and np.abs(det_outer) > 0.01:
	# 		n_nonsingular+=1
	# 		print('nondegenerate below:')
	# 	print(f'det inner={det_inner:5.1f} and outer={det_outer:5.1f}')
	# 	# print(X)
	# 	# print(y)
	# print(n_nonsingular)