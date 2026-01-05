import sys
import numpy as np


#for part 2 dijkstra's algorithm should still work.
#except that now we have a much larger graph since nodes
#are combinations of joltages up to the maximum values. 
#so...let me first investigate the result.

#implement dijkstra's algorithm.
#on switchboards with states that are nodes 
#which are actually binary numbers
#
#The 'edges' are the connections provided by the wiring diagram.
#I read the wikipedia page on this which was helpful.

class Node:
	def __init__(self, n=None, d=float('inf'), N=None,prev=None):
		self.n=n #id number (binary number of length N)
		self.d=d #distance from start.
		self.N=N #length of the binary number (number of indicator lights)
		self.prev=prev #keep track of the previous node...for returning the path

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
	#I will avoid implementing __eq__ for now.
	def equals(self, other: "Node"):
		if self.n==other.n:
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

def get_neighbor_idx_in_graph(node, graph=None, C=None):
		if C==None:
			C=[]

		if graph==None:
			graph=[]

		neighbors=[]
		for keypress in C: #C buttons should have the same length as current instance of the node.
			#don't mix them up...
			neighbor_n=node.n^keypress #press the key = xor
			neighbors.append(neighbor_n)

		indices=[]
		for neighbor in neighbors: 
			for i in range(len(graph)):
				if neighbor==graph[i].n:
					indices.append(i)
		return indices

def print_graph(graph: list["Node"]):
	print(f'Graph of length {len(graph)} printing:')
	for node in graph:
		print(f'Graph has node {node.n}, bin: {node} with distance {node.d}')
	return None

def dijkstra(indicator_lights, button_list):
	lights=indicator_lights
	N=len(lights)
	start=Node(n=0,d=0,N=N)
	finish=Node(int(lights,2),d=INF,N=N)
	#C is the list of button connections (which are conveniently also binary numbers)
	C=get_connections(button_list,N=N)

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



	INF=float('inf')

	# print(LIGHTS)
	# print(JOLTAGES)
	# print(BUTTONS[0])
	###

	# IDX=0
	# joltages=JOLTAGES[IDX]
	# button_list=BUTTONS[IDX]

	#investigate input
	# num_nodes=[]
	# for joltages in JOLTAGES:
	# 	y=[float(a) for a in joltages]
	# 	x=np.prod(y)
	# 	print(f'j: {joltages} : p: {x}')

	# 	num_nodes.append(x)

	# print(num_nodes)
	# print(f'max = {max(num_nodes)}')
	# print(f'length = {len(num_nodes)}')

	#it is impossible (and inefficient) to initialize 
	#all nodes up to all the joltages. for some cases,
	#there are 10^21 combinations...

	#but maybe we can simplify the problem. 
	#think about the path from finish to start...
	#and count all the button presses in reverse 
	#take the longest button and (un)press it as many times as you can
	#until one of the numbers is zero (but not all probably)
	#then take the next longest ...
	#obviously you want to press the longest as many times since by pressing
	#the longest button you increase the joltages most quickly.
	#at the end of this process you won't have all zeros, but you will
	#have a new target that may be possible to dijkstra to with the existing code.
	# let's check.



	IDX=0
	joltages=JOLTAGES[IDX]
	button_list=BUTTONS[IDX]

	print(f'initial j: {joltages}')
	while button_list:
		button_lengths=[len(x) for x in button_list]
		i=max(range(len(button_lengths)), key=button_lengths.__getitem__)
		button=button_list.pop(i)

		min_joltage=INF
		for i,b in enumerate(button):
			j=joltages[b]
			if j<min_joltage:
				min_joltage=j
		npresses=min_joltage
		for b in button:
			joltages[b]-=min_joltage
		print(f'pressed button {button} n={npresses} times.')
		print(f'j: {joltages}')

	# that doesn't work...obviously. it leaves us the unsolvable
	# reminder. that's the whole point of graphs. 

	#but after checking the subreddit - I avoided spoilers, 
	#people spoke about linear algebra and using something to solve for it
	#let me see if I can design my own solution based on it.
	#this is in the end just a linear equation

	for button_list, joltages in zip(BUTTONS, JOLTAGES):
		print(len(button_list), len(joltages))
		
	# total_distance=0
	# for idx in range(len(LIGHTS)):
	# 	d=dijkstra(LIGHTS[idx],BUTTONS[idx])
	# 	total_distance+=d

	# print('-'*20)
	# print(f'final result is {total_distance}')
	# print('-'*20)
	


