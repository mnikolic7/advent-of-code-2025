import sys

#implement dijkstra's algorithm.
#on switchboards with states that are nodes 
#which are actually binary numbers
#
#The 'edges' are the connections provided by the wiring diagram.

class Node:
	def __init__(self, n=None, d=float('inf'), N=None):
		self.n=n #id number (binary number of length N)
		self.d=d #distance from start.
		self.N=N #length of the binary number (number of indicator lights)

	def get_neighbors(self, C=None):
		if C==None:
			C=[]

		neighbors=[]
		for keypress in C: #C buttons should have the same length as current instance of the node.
			#don't mix them up...

			neighbor=self.n^keypress #press the key = xor
			neighbor=Node(n=neighbor, N=self.N, d=self.d+1)
			neighbors.append(neighbor)
		return neighbors

	#define equals method check if the id of two instances of Node
	# is the same, and we will use this to keep only one instance.
	#and just to be safe, check that N is the same, but that
	#should be common for everything...
	#I will avoid implementing __eq__ for now
	def equals(self, other: "Node"):
		if self.n==other.n and self.N==other.N:
			return True
		else:
			return False

	def __str__(self):
		return format(self.n ,f'0{self.N}b')

def get_connections(C: list[int],N=None):
	result=[]
	if N is None:
		raise ValueError('Please provide N-number of lights')

	for conn in C:
		curr_val=['0']*N
		for idx in conn: curr_val[idx]='1'
		curr_val=''.join(curr_val)
		curr_val=int(curr_val,2)
		result.append(curr_val)
	return result

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

	# print(LIGHTS)
	# print(JOLTAGES)
	# print(BUTTONS[0])
	###

	IDX=0
	lights=LIGHTS[IDX]
	button_list=BUTTONS[0]

	INF=float('inf')

	#create a graph: no need to make anything for all nodes.
	#all nodes are binary numbers of length N.
	# we only care about the current nodes and neighbors...
	# so we will keep track of only initialized ones.
	N=len(lights)
	#starting node is 0000, it's distance is zero.
	#all other nodes distance is inf.
	start=Node(n=0,d=0,N=N)
	#but initialize only one, and then as we go we will initialize as we need.
	finish=Node(int(lights,2),d=INF,N=N)
	#C is the list of button connections (which are conveniently also binary numbers)
	C=get_connections(button_list,N=N)

	#take the start node.
	#find neighbors.
	#for each neighbor, check if it is in the list of visited.
	#if yes, update its distance to min(its distance, distance from current node)
	#if not, just add to the list of visited.
	#stop when you reach the final node.

	#breadth first search - think about this...
	#first step


	# visited=[start]
	# found = False
	# while not found:
	# 	#go through visited nodes and use them as a start
	# 	# for current_start in visited:

	# 	#this is a bit weird since len of visited might increase
	# 	#inside the loop, but keep going until you find.
	# 	#there is probably a better way to write this through recursion.
	# 	i=0
	# 	while i < len(visited): 
	# 		current_start=visited[i]
	# 		print(f'curr start = {current_start.n} bin: {current_start}')
	# 		if current_start.equals(finish):
	# 			found=True
	# 			print('-'*30)
	# 			print(f'min_number_of_steps={current_start.d}')
	# 			print('-'*30)
	# 			break
	# 		neighbors=current_start.get_neighbors(C=C)
	# 		#for each neighbor of the current start,
	# 		#check if it has been visited.
	# 		for neigh in neighbors:
	# 			print(f'curr_neigh={neigh.n} bin:{neigh}')
	# 			for v in visited:
	# 				# print(f'neigh={neigh.n} bin: neigh')
	# 				print(f'v={v.n} bin: {v}')
	# 				if neigh.equals(v):
	# 					print(f'cur_dist={neigh.d}, and visited_dist={v.d}')
	# 					v.d=min(v.d,neigh.d)
	# 					print(f'new dist of v is {v.d}')
	# 				else:
	# 					print(f'{neigh.n} bin: {neigh} not visited before')
	# 					print(f'added {neigh} to visited')
	# 					visited.append(neigh)
	# 		i+=1
