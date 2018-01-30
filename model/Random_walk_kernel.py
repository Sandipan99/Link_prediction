import graph as g
import numpy as np
import scipy as sc
import networkx as nx
import metrics

def random_walk(G,l,s,v,f_v,dim):
	if l==0:
		return f_v[v]
	else:	
		sum_ = np.zeros(dim)
		for u in nx.all_neighbors(G,v):
			if u!=s: 
				sum_ = np.add(sum_,random_walk(G,l-1,v,u,f_v,dim))
		return np.multiply(f_v[v],sum_)

def Random_walk_kernel(G, length, decay, f_v, dim):
	nodes = G.nodes()
	node_vector = f_v
	decay = decay ** (length - 1)
	l = length - 1
	for i in xrange(len(nodes)):
		v = nodes[i]
		vector = random_walk(G,l-1,v,v,f_v,dim)
		node_vector[v] = decay*vector
		print "obtained vector for: ",v,"- ",node_vector[v]
	return node_vector

if __name__=="__main__":

	
	G,G_t = g.obtain_graph_single("Data/Facebook/facebook_combined.txt",0.25)
	print G.number_of_edges(), len(G.nodes()), G_t.number_of_edges(), len(G_t.nodes())

	dim = 5
	length = 5
	decay = 0.8
	
	w,f_v = g.obtain_node_features(G_t,dim)

	print w.real
	print f_v[0],f_v[1]

	#node_vectors = Random_walk_kernel(G_t, length, decay, f_v, dim)

	#MAP = metrics.evaluate(G,G_t,node_vectors, t_h)	
	'''

	G = nx.Graph()
	G.add_edge(1,2)

	G.add_edge(2,3)

	G.add_edge(2,6)

	G.add_edge(3,4)

	G.add_edge(3,5)

			
	f_v = {}

	f_v[1] = np.array([1,2])

	f_v[2] = np.array([1,3])

	f_v[3] = np.array([3,2])

	f_v[4] = np.array([4,6])

	f_v[5] = np.array([5,1])

	f_v[6] = np.array([2,6])
	
	vector = random_walk(G,3,1,1,f_v,2)

	print vector
	'''
