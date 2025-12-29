import sys
import math
import numpy as np
import matplotlib.pylab as plt

'''
ok so my way was good. I implemented something that chatGPT calls
DSU (disjoint set union). That's great. My solution was nice, but needs
a few improvements which I will implement here.
# DSU has two operations: merge and find_root
DSU keeps track of the parent and if there is no parent, then the 
item is root.
Optimizations:
1) merging two things is easy - checks if the roots are the same, and 
   if not, merges the smaller one to the larger one. this makes the tree
   depth grow slow and find is roughly O(log(N)) intead of O(N)
   without it.
2) whenever you use find(), just make everything point to the root
	then this is super fast, because it almost becomes O(1)

then I will keep the N^2 calculation of distances, and just slightly
modify this to run continuously until everything is connected.
then the final result will be straightforward.
''' 

#find with path compression
def find_root(id):
	if circuit_ID[id]==id:
		return id
	else:
		root=find_root(circuit_ID[id]) #recursively find root
		circuit_ID[id]=root #compress path
		return root

def merge(id1,id2):
	r1=find_root(id1)
	r2=find_root(id2)

	if r1==r2: #already connected
		return 

	s1=circuit_sizes[r1]
	s2=circuit_sizes[r2]
	if s1<s2:
		r1,r2=r2,r1
		#r2 is smaller now
	
	circuit_ID[r2]=r1 #point r2 to r1
	circuit_sizes[r1]=s1+s2 #only roots have valid sizes.

def get_root_idx():
	return [circuit_ID[i]==i for i in range(len(circuit_ID))]

def get_root_sizes():
	return circuit_sizes[get_root_idx()]

#solution to part2 of day 8, 2025
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
	#let me solve this in my own style. no linked list. 
	#just lists of IDs. I will have to "walk the dog anyway"

	#keep arrays for the DSU implementation.
	circuit_ID=np.arange(N_points) #which circuit does the nth point belong to?
	circuit_sizes=np.ones(N_points) #what is the size of each circuit. 

	#now this is super simple. :) 
	for i in idx:
		id1=iu[i]
		id2=ju[i]	
		#find all indices with roots at circuit ID
		root1=find_root(id1)
		root2=find_root(id2)
		#merge
		merge(root1,root2)

	valid_sizes=get_root_sizes()
	print('final result:')
	print(np.partition(valid_sizes,-3)[-3:])
	print(np.prod(np.partition(valid_sizes,-3)[-3:]))
