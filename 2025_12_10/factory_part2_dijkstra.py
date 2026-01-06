import sys
import numpy as np

#implement dijkstra's algorithm.
#on switchboards with states that are nodes 

#The 'edges' are the connections provided by the wiring diagram.

#start at final joltages
#imagine every key press goes in reverse: i.e. decreases the buttons by 1
#find the shortest path to zero. 
#return that. 

#the problem here is that I implemented the original dijkstra's algorithm for part 1
#which is O(V^2) where V is number of vertices.
#for part 1, V was at most 1024, so that worked fine.
#here V can be 10^21, which would make it too long for the given input.
#but it should work.

#nonetheless, it is easy to implement for shorter paths,
#but I must implement the optimization for the queue.
#and adapt the nodes to implement integer sequences instead of binary numbers

class Node:
	def __init__(self, n=None, d=float('inf'), N=None,prev=None):
		if N==None:
			raise ValueError('provide valid N to Node')
		#id number (binary number of length N)
		if n==None:
			self.joltage=[0]*N
		else:
			self.joltage=n
		self.d=d #distance from start.
		self.N=N #length of the joltage indicator (number of indicator lights)
		self.prev=prev #keep track of the previous node...for returning the path

	#define equals method check if the id of two instances of Node
	# is the same, and we will use this to keep only one instance.
	#I will avoid implementing __eq__ for now.
	def equals(self, other: "Node"):
		for n1,n2 in zip(self.joltage,other.joltage)
			if n1!=n2:
				return False
		result=True

	def __str__(self):
		return f'Node with joltages {self.joltage}'

# def get_connections(C: list[int],N=None):
# 	result=[]
# 	if N is None:
# 		raise ValueError('Please provide N-number of lights')

# 	for conn in C:
# 		curr_val=['0']*N
# 		for idx in conn: curr_val[idx]='1'
# 		curr_val=''.join(curr_val)
# 		curr_val=int(curr_val,2)
# 		result.append(curr_val)
# 	return result

def get_neighbor_idx_in_graph(node, graph=None, C=None):
		if C==None:
			C=[]

		if graph==None:
			graph=[]

		neighbors=[]
		for keypress in C: #C buttons should have the same length as current instance of the node.
			#don't mix them up...
			for i in range(node.N):
				neighbor_n=node.n^keypress #press the key = xor
			neighbors.append(neighbor_n)

		indices=[]
		for neighbor in neighbors: 
			for i in range(len(graph)):
				if neighbor==graph[i].n:
					indices.append(i)
		if indices:
			return indices
		else:
			return -1

def print_graph(graph: list["Node"]):
	print(f'Graph of length {len(graph)} printing:')
	for node in graph:
		print(f'Graph has node {node.n}, bin: {node} with distance {node.d}')
	return None

def dijkstra(indicator_lights, button_list):
	lights=indicator_lights
	#create a graph: no need to make anything for all nodes.
	#all nodes are binary numbers of length N.
	# we only care about the current nodes and neighbors...
	# so we will keep track of only initialized ones.

	#by observing the input there are at most 10 switches at once.
	#so...at most 1024 possible states. So it is possible to simply initialize the entire graph.
	#so I will make the whole graph
	#and this will help me avoid being stuck in the infinite loop.
	N=len(lights)
	#starting node is 0000, it's distance is zero.
	#all other nodes distance is inf.
	start=Node(n=0,d=0,N=N)
	#but initialize only one, and then as we go we will initialize as we need.
	finish=Node(int(lights,2),d=INF,N=N)
	#C is the list of button connections (which are conveniently also binary numbers)
	C=button_list

	#take the start node.
	#find neighbors.
	#for each neighbor, check if it is in the list of visited.
	#if yes, update its distance to min(its distance, distance from current node)
	#if not, just add to the list of visited.
	#stop when you reach the final node.

	#breadth first search - think about this...
	#first step

	dist=[INF]*(2**N)
	graph=[start]
	visited=[]
	for i in range(1,2**N):
		graph.append(Node(n=i,d=INF,N=N))
		# print(graph[i])

	print(f'target is {finish}, in decimal: {finish.n}')
	while graph: #while graph is not empty
		if all([x.d==INF for x in graph]):
			#if all remaining nodes are inaccessible...
			break

		d=[x.d for x in graph]
		# i=np.argmin(d)
		i = min(range(len(d)), key=d.__getitem__)
		
		curr_node=graph.pop(i)
		visited.append(curr_node)
		# print_graph(graph)
		# print('visited:')
		# print_graph(visited)
		if finish.equals(curr_node):
			print('-'*30)
			print(f'dist to target = {curr_node.d}')
			dist_to_target=curr_node.d
			print('-'*30)
			break

		indices=get_neighbor_idx_in_graph(curr_node, graph=graph, C=C)

		for idx in indices:
			alt_dist=curr_node.d+1
			if alt_dist<graph[idx].d:
				graph[idx].d=alt_dist
				graph[idx].prev=curr_node
		# print('graph at the end of loop')
		# print_graph(graph)

	return dist_to_target



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

	# IDX=2
	# lights=LIGHTS[IDX]
	# button_list=BUTTONS[IDX]


	INF=float('inf')
	total_distance=0
	for idx in range(len(LIGHTS)):
		d=dijkstra(LIGHTS[idx],BUTTONS[idx])
		total_distance+=d

	print('-'*20)
	print(f'final result is {total_distance}')
	print('-'*20)
	


