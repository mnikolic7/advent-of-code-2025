import sys
import math
import numpy as np
import matplotlib.pylab as plt

class jbox:
	def __init__(self, ID=None):
		self.ID=ID
		self.connections=[]
		self.circuit_size=1

	def connect(self, other: "jbox"):
		if other is self:
			return

		if other not in self.connections:
			self.connections.append(other)
			other.connections.append(self)

		total_size=self.circuit_size+other.circuit_size
		self._propagate_circuit_size(total_size)
		other._propagate_circuit_size(total_size)

	def _propagate_circuit_size(self, size):
		if self.circuit_size == size:
			return
		self.circuit_size= size 
		for jb in self.connections:
			jb._propagate_circuit_size(size)

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


	N_connections=1000
	#solution 1: almost brute force. N^2 to calculate D, and then NlogN to search for smallest N
	
	#ok, so if v=[x,y,z] is the vector of positions
	#then |v2-v1|^2 = |v2|^2 + |v1|^2 - 2* (v1 dot v2)
	#I can do that efficiently in numpy if I order all the vectors in a matrix
	# P = [v1,v2,v3...] and M is a vector =[|v1|^2, |v2|^2, ...]
	
	#note: I imagine vectors to be vertical - so one vector is a column. 
	#I am aware that columns are the second axis in python, and it's maybe slightly less efficient than thinking in Transpose, but I can't.

	#then M+M^T will have entries M_ij=[|vi|^2 + |vj|^2] 
	#P*P^T = will have entries: [vi*vj]
	
	M=np.sum(P**2,axis=0)
	D=M[np.newaxis,:]+M[:,np.newaxis]-2*P.T@P
	D=np.sqrt(D)
	# print(D)

	#find indices of M smallest D's

	[iu, ju]=np.triu_indices_from(D,k=1)

	distances=D[iu,ju]
	idx=np.argpartition(distances, N_connections)[:N_connections]
	# idx=idx[np.argsort(distances[idx])]


	_,K=P.shape
	# JBoxes=[]
	# for j in range(K):
	# 	JBoxes.append(jbox(ID=j)) 

	# max_sizes=np.ones(3)
	# for i in idx:
	# 	JBoxes[iu[i]].connect(JBoxes[ju[i]])
	# 	new_size=JBoxes[iu[i]].circuit_size

	# 	if new_size>min(max_sizes):
	# 		print(f'new size {new_size}')
	# 		max_sizes[np.argmin(max_sizes)]=new_size

	# print(max_sizes)
	# print(np.prod(max_sizes))
	# print('-'*20)



	##
	fig=plt.figure()
	ax=fig.add_subplot(projection='3d')

	
	k=np.random.randint(0,K,K//2)


	for i in idx:
		x1=P[0,iu[i]]
		x2=P[0,ju[i]]
		y1=P[1,iu[i]]
		y2=P[1,ju[i]]
		z1=P[2,iu[i]]
		z2=P[2,ju[i]]
		ax.plot([x1,x2],[y1,y2],[z1,z2],'g-',linewidth=3)
	# plt.matshow(D)
	# ax.grid(False)
	ax.plot(P[0,:],P[1,:],P[2,:],'ko',markersize=3,markerfacecolor='red')
	ax.plot(P[0,k],P[1,k],P[2,k],'ko',markersize=3,markerfacecolor='gold')
	plt.show()



	#solution 2 would include kd-trees which I will just leave for the second part.
	# it might be easiest to just use sklearn or scipy, but when/if I have time, I maybe write my own implementation, which would be pedagogical.