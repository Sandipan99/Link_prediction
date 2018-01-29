import graph as g
import numpy as np
import scipy as sc
import networkx as nx
import metrics

def Random_walk_kernel(G, length, decay, f_v):
	nodes = G.nodes()
	node_vector_dict = {}
	node_vector = f_v
	for i in xrange(len(nodes)):
		l = length
		v = nodes[i]
		while(l>0):
			vec_all = np.zeros(np.shape(f_v)[0])
			for u in nx.all_neighbors(G,v):
				vec_all = np.add(vec_all,f_v[nodes.index(u)])
			node_vector[i] = np.multiply(node_vector[i],vec_all)
			l-=1
		node_vector_dict[v] = node_vector[i]
	return node_vector_dict

if __name__=="__main__":

	G,G_t = g.obtain_graph_single("text file")
	
	f_v = g.obtain_node_features(G_t)

	node_vectors = Random_walk_kernel(G_t, length, decay)

	MAP = metrics.evaluate(G,G_t,node_vectors, t_h)	
		
