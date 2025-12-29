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
		return r1

	s1=circuit_sizes[r1]
	s2=circuit_sizes[r2]
	if s1<s2:
		r1,r2=r2,r1
		#r2 is smaller now
	
	circuit_ID[r2]=r1 #point r2 to r1
	circuit_sizes[r1]=s1+s2 #only roots have valid sizes.
	#optionally return the root of the merged circuits.
	return r1

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

	circuit_ID=np.arange(N_points) #which circuit does the nth point belong to?
	circuit_sizes=np.ones(N_points)#what is the size of each circuit. 
	#part 2:
	idx=np.argsort(distances)

	for i in idx:
		id1=iu[i]
		id2=ju[i]

		r1=find_root(id1)
		r2=find_root(id2)
		# print(f'merging    : {id1} and {id2}')
		# print(f'with roots : {r1} and {r2}')
		# print(f'circ_ID:   :', circuit_ID)
		# print(f'sizes      :', circuit_sizes)
		# print(f'sizes maskd:', circuit_sizes*np.array(get_root_idx()))

		final_root=merge(r1,r2)
		# print(f'after merging')
		# print(f'circ_ID:   :', circuit_ID)
		# print(f'sizes      :', circuit_sizes)
		# print(f'sizes maskd:', circuit_sizes*np.array(get_root_idx()))
		# print(final_root)
		if circuit_sizes[final_root]==N_points:
			final_id1=id1
			final_id2=id2
			print('DONE!')
			break
	#this should work
	print(P[0,final_id1]*P[0,final_id2])
