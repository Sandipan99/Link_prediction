import networkx as nx
import numpy as np
from numpy import linalg as LA

def obtain_unique_id(fname):


def obtain_graph(fname):
	graph_list = [nx.Graph() for i in xrange(24)]
	fs = open(fname)
	for line in fs:
		u,v,t = map(int,line.strip().split("\t"))
		if t<1989:
			continue
		else:
			t = t-1989
			graph_list[t].add_edge(u,v)

	return graph_list

def obtain_node_features(G,n):
	L_mat = nx.normalized_laplacian_matrix(G)
	w,v = LA.eig(L_mat)
	return v[:,:n]	

if __name__=="__main__":
	G = obtain_graph()
