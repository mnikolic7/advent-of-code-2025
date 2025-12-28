import sys
import math
import numpy as np
import matplotlib.pylab as plt

'''
#ok, so I was complicating. I learned about KD-trees but I didn't fully 
#understand how to implement them, and then I got stuck reading/chasing 
#my own tail. 

Today (12/28/25) I spoke with moln-r who told me - just do a simple 
linked list, which will be best. Simple, somewhat inefficient solution 
will get me there. Better to solve it, than to dabble in things I can 
learn later...that's the exercise now. Actually, forget linked lists.
I will just do my own thinking.
''' 


#solution to part1 of day 8, 2025
if __name__=="__main__":
	fname=sys.argv[1]

	lines=[]
	with open(fname, 'r') as f:
		for line in f:
			lines.append(line.strip())

	P=np.zeros((3,len(lines))) #positions matrix
	for i,line in enumerate(lines):
		x,y,z=line.split(',')
		P[:,i]=[int(x),int(y),int(z)]

	_,N_points=P.shape
	N_connections=1000
	#solution 1: somewhat brute force. N^2 to calculate D, and then 
	#NlogN to search for smallest distances.
	
	#ok, so if v=[x,y,z] is the vector of positions
	#then |v2-v1|^2 = |v2|^2 + |v1|^2 - 2* (v1 dot v2)
	#I can do that efficiently in numpy if I order all the vectors in a 
	#matrix
	# P = [v1,v2,v3...] and M is a vector =[|v1|^2, |v2|^2, ...]
	
	#note: I imagine vectors to be vertical - so one vector is a column. 
	#I am aware that columns are the second axis in python, and it's 
	#maybe slightly less efficient than thinking in Transpose, but I 
	#can't.

	#then M+M^T will have entries M_ij=[|vi|^2 + |vj|^2] 
	#P*P^T = will have entries: [vi*vj]
	
	M=np.sum(P**2,axis=0)
	D=M[np.newaxis,:]+M[:,np.newaxis]-2*P.T@P
	# D=np.sqrt(D) #not really needed.
	# print(D)

	#find indices of M smallest D's

	[iu, ju]=np.triu_indices_from(D,k=1)

	distances=D[iu,ju] #this is ravelled already. 
	#(ravelled==unravelled, english is funny)

	#numpy.partition(arr, n) takes the n_th smallest item in arr, and 
	#returns an array such that all smaller items are before it and 
	#and larger are after it. neither left nor right side are sorted.
	#it's cheap sorting. 
	#np.argpartition returns the indices of this rearrangement. 
	idx=np.argpartition(distances, N_connections)[:N_connections]
	# [:N_connections] means we only need the left side.
	idx=idx[np.argsort(distances[idx])] #sort indices in idx
	for i in idx:
		print(iu[i],ju[i])

	print('---')
	#let me solve this in my own style. no linked list. 
	#just lists of IDs. I will have to "walk the dog anyway"

	circuit_ID=np.arange(N_points) #which circuit does the nth point belong to?
	circuit_sizes=np.ones(N_points)#what is the size of each circuit. 


	for i in idx:
		id1=iu[i]
		id2=ju[i]
		
		#if id1 and id2 are in the same circuit do nothing
		if circuit_ID[id1]==circuit_ID[id2]:
			continue
		
		#else, add id2 to id1's circuit. 
		
		#first, check which one is smaller and add smaller to the larger. 
		if circuit_sizes[id2]>circuit_sizes[id1]:
			id2,id1=id1,id2 #python idiom. python evaluates rhs first!
			#instead of:
			# id_temp=id2
			# id2=id1
			# id1=id_temp

		id2_list=np.where(circuit_ID==circuit_ID[id2])
		id1_list=np.where(circuit_ID==circuit_ID[id1])

		curr_size=circuit_sizes[id2]+circuit_sizes[id1]

		circuit_sizes[id2_list]=curr_size
		circuit_sizes[id1_list]=curr_size
		circuit_ID[id2_list]=circuit_ID[id1]
		#circuit_ID[id1_list]=circuit_ID[id1] #redundant, left for clarity

	_,indices=np.unique(circuit_ID,return_index=True)
	print('final result:')
	print(np.partition(circuit_sizes[indices],-3)[-3:])
	print(np.prod(np.partition(circuit_sizes[indices],-3)[-3:]))
