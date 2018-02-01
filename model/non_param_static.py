import networkx as nx
import graph as g
import metrics
import numpy as np
import math

def calculate_feature_probability(G_t, f_v):
	feat_bucket_ita = {}
	feat_bucket_ita_p = {}
	nodes = G_t.nodes()
	for i in xrange(len(nodes)-1):
		for j in xrange(i+1,len(nodes)):
			x = np.dot(f_v[nodes[i]],f_v[nodes[j]])
			b = metrics.sigmoid(x)	
			#b = calculate bucket
			if b not in feat_bucket_ita:
				feat_bucket_ita[b] = 1
				feat_bucket_ita_p[b] = 0
			else	feat_bucket_ita[b] += 1

			if G_t.has_edge(nodes[i],nodes[j]):
				feat_bucket_ita_p[b] += 1

	return feat_bucket_ita, feat_bucket_ita_p


if __name__=="__main__":

	G,G_t = g.obtain_graph_single("Data/Facebook/facebook_combined.txt",0.25)
	f_v = g.obtain_node_features(G_t,n)
	
	feat_b_ita, feat_b_ita_p = calculate_feature_probability(G_t, f_v)
		
	print metrics.evaluate_non_param(G,G_t,f_v,feat_b_ita,feat_b_ita_p,t_h)


