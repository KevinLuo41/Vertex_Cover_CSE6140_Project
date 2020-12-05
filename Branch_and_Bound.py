import random
import time


# find the vertex with max degree in the remain G as new candidate node
def find_candidate(g):
	deglist_sorted = sorted(g.degree, reverse=True, key=lambda x: x[1])  # sort in descending order of node degree
	v = deglist_sorted[0]  
	return v[0]

def find_candidate_size(g):
	deglist_sorted = sorted(g.degree, reverse=True, key=lambda x: x[1])  # sort in descending order of node degree
	v = deglist_sorted[0]  
	return v[1]	

#lower_bound after ceiling
import math
def lower_bound(graph):
	lb = graph.number_of_edges() / find_candidate_size(graph)
	lb = math.ceil(lb)
	return lb

#CALCULATE SIZE OF VERTEX COVER (NUMBER OF NODES WITH STATE=1)
def size(VC):
	size = 0
	for element in VC:  # VC is a tuple list, where each tuple = (node_ID, state, (node_ID, state))
		size +=  element[1]
	return size

class BnB:
	def __init__(self, G,  # Graph
				out_dir="./OUT/BnB_out/",  # output dir
				cut_off=60,  # cut off time
				seed=1,  # random seed
				):

		random.seed(seed)

		self.G = G
		self.cut_off = cut_off
		self.out_dir = out_dir


	def search(self):
		# Generate global time
		start_time=time.time()
		end_time=start_time
		execution_time=end_time-start_time
		trace=[]    #list of trace when solution is found, tuple=(VC size,execution_time)

		# initialization of containners
		optimal_VC = []
		current_VC = []
		Frontier = []
		UpperBound = self.G.number_of_nodes() # initialization of UPPER BOUND(total nodes of the graph)

		remain_g = self.G.copy()  # initial remain_g, which is a copy of G
		v = find_candidate(remain_g)	# sort dictionary of degree of nodes to find node 

		# initialize FRONTIER
		Frontier.append((v, 0, (-1, -1)))  # tuples of {node,state,(parent vertex,parent vertex state)}, here we don't choose it
		Frontier.append((v, 1, (-1, -1)))  # tuples of {node,state,(parent vertex,parent vertex state)}, here we choose it.


		while Frontier != [] and execution_time < self.cut_off:
			backtrack = False
			curr, state, _ = Frontier.pop() #pop out the last element in Frontier as current vertex

		
			if state == 0:  # if curr is not selected, select all the neighbors to vc
				for node in list(remain_g.neighbors(curr)):
					current_VC.append((node, 1))
					remain_g.remove_node(node)  # node is in VC, remove neighbors from remain_g
			else: # if curr is selected, remove all neighbors out of remain_g
				remain_g.remove_node(curr)  # curr is in VC,remove node from G
			
			current_VC.append((curr, state))     # add it to  vc
			
			current_VC_size = size(current_VC)

			if remain_g.number_of_edges() == 0:  # no edges are left in remain_g, which means solution found

				if current_VC_size < UpperBound:
					optimal_VC = current_VC.copy()
					print('Current Opt VC size', current_VC_size)
					UpperBound = current_VC_size
					trace.append((current_VC_size, time.time()-start_time))
				backtrack = True
					
			else:   # partial solution
				current_lb = lower_bound(remain_g) + current_VC_size

				if current_lb < UpperBound:  # not pruning
					next = find_candidate(remain_g)
					Frontier.append((next, 0, (curr, state))) #(curr,state) is parent of next
					Frontier.append((next, 1, (curr, state)))
				else:
					# prune this path,backtrack to its parent
					backtrack=True

			if backtrack==True:
				if Frontier == []:	# if we get the start, we cannot backtrack further， then we are done
					print('-----Done!!!-----')
				else:	
					next_parent = Frontier[-1][2]	#parent of last element in Frontier (tuple of (vertex,state))

					# backtrack to the level of next_parent
					if next_parent in current_VC:
						
						index_parent = current_VC.index(next_parent) # returns the index (from 1)of parent in current_VC
						while index_parent < len(current_VC) - 1:	# undo changes from end of current_VC back up to parent node
							mynode,_ = current_VC.pop()	# undo the addition to current_VC
							remain_g.add_node(mynode)	# undo the deletion from remain_g
							
							# find all the edges connected to curr in Graph G
							# or the edges that connected to the nodes that not in current VC set.
							
							current_VC_nodes = list(map(lambda x:x[0], current_VC))
							for nd in self.G.neighbors(mynode):
								if (nd in remain_g.nodes()) and (nd not in current_VC_nodes):
									remain_g.add_edge(nd, mynode)	#recover the node which is deleted from the remain_g

					elif next_parent == (-1, -1):
						# backtrack to the root node
						current_VC.clear()
						remain_g = self.G.copy()
					else:
						print('error in backtracking step')

			end_time=time.time()
			execution_time = end_time-start_time
			if execution_time > self.cut_off:
				print('Cutoff time reached')
		# select only the vertex from the optimal vc.
		optimal_VC_vertex = []	
		for element in optimal_VC:
			if element[1]==1:
				optimal_VC_vertex.append(element[0])
		return optimal_VC_vertex,trace 