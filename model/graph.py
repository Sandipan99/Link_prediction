import networkx as nx
import numpy as np
from numpy import linalg as LA
import scipy as sp
import random

def obtain_graph(fname):
	graph_list = [nx.Graph() for i in xrange(24)]
	fs = open(fname)
	for line in fs:
		u,v,t = map(int,line.strip().split("\t"))
		if t<1989:
			continue
		else:
			t = t-1989
			print "inserting ",u," ",t," ",v
			graph_list[t].add_edge(u,v)
	fs.close()
	return graph_list

def obtain_node_features(G,n):
	L_mat = nx.normalized_laplacian_matrix(G)
	w,v = sp.sparse.linalg.eigs(L_mat,n)
	return v.real	

def obtain_graph_single(fname, t_h):
	G = nx.Graph()  #contains all edges
	G_t = nx.Graph() #contains only the training set t_h fraction of all edges

	fs = open(fname)
	for line in fs:
		u,v = map(int,line.strip().split())
		G.add_edge(u,v)
		if random.uniform(0,1)> t_h:
			G_t.add_edge(u,v)
	fs.close()

	return G,G_t
	

if __name__=="__main__":
	G = obtain_graph("../network_algorithm_author_citation_www.txt")
	eig_vec = obtain_node_features(G[1],5)
	for i in xrange(24):
		print len(G[i].nodes())
