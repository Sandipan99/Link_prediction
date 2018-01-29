import numpy as np
from scipy import spatial

def find_sample(G,G_t,u,nodes):
	sample = []
	nbr_g = nx.all_neighbors(G_t,u)
	nbr_p = filter(lambda x:x not in nbr_g, nx.all_neighbors(G,u))
	cnt = t_h*len(nbr_p) - len(nbr_p)
	while(cnt>0):
		random.shuffle(nodes)
		for n in nodes:
			if (n!=u)and(n not in nbr_g)and(n not in nbr_p):
				sample.append(n)
				cnt--
	sample = sample + nbr_p
	return sample,len(nbr_p)

def average_precision(G,edge_score,q_u):
	cnt = 0
	cnt_p = 0
	pres = 0.0
	for v,score in sorted(edge_score.items(),key = lambda x:x[1], reverse=True):
		cnt+=1
		if G.has_edge(q_u,v):
			cnt_p+=1
			pres+=float(cnt_p)/cnt
	return pres/cnt

def evaluate(G,G_t,node_vectors,t_h):
	q_nodes = G_t.nodes()
	MAP = 0.0
	for q_u in q_nodes:
		sampled_nodes,L = find_sample(G,G_t,u,q_nodes,t_h)
		vec_u = node_vectors[q_u]
		edge_score = {}
		for v in sampled_nodes:
			vec_v = node_vectors[v]
			score = 1 - spatial.distance.cosine(vec_u,vec_v)
			edge_score[v] = score
		avg_prec = average_precision(G,edge_score,q_u)
		MAP+=(1.0/L)*avg_prec

	return MAP/len(q_nodes)
			
