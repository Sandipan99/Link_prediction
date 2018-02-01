import numpy as np
from scipy import spatial
import math

def find_sample(G,G_t,u,nodes):
	sample = []
	nbr_g = nx.all_neighbors(G_t,u)
	nbr_p = filter(lambda x:(x not in nbr_g)and(x in nodes), nx.all_neighbors(G,u))
	cnt = t_h*len(nbr_p) - len(nbr_p)
	random.shuffle(nodes)
	for n in nodes:
		if (n!=u)and(n not in nbr_g)and(n not in nbr_p):
			sample.append(n)
			cnt-=1
			if cnt==0:
				break
		
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

def sigmoid(x):
	return 1/(1 + math.exp(-x));

def TV_distance(i_t,j_t):
	return math.fabs(i_t - j_t)

def cal_probability(feat_b_ita, feat_b_ita_p, b):
	num_s = 0.0
	den_s = 0.0
	i_t = float(feat_b_ita_p[b])/feat_b_ita[b]
	for s in feat_b_ita:
		j_t = float(feat_b_ita_p[s])/feat_b_ita[s] 
		den_s += TV_distance(i_t,j_t)
		if feat_b_ita_p[s]>0:
			num_s += TV_distance(i_t,j_t)
	return num_s/den_s

def evaluate(G,G_t,node_vectors,t_h):
	q_nodes = G_t.nodes()
	MAP = 0.0
	for q_u in q_nodes:
		sampled_nodes,L = find_sample(G,G_t,u,q_nodes,t_h)
		vec_u = node_vectors[q_u]
		edge_score = {}
		for v in sampled_nodes:
			vec_v = node_vectors[v]
			x = np.dot(vec_u,vec_v)
			score = sigmoid(x)
			edge_score[v] = score
		avg_prec = average_precision(G,edge_score,q_u)
		MAP+=(1.0/L)*avg_prec

	return MAP/len(q_nodes)

def evaluate_non_param(G,G_t,f_v,feat_b_ita,feat_b_ita_p,t_h):
	q_nodes = G_t.nodes()
	MAP = 0.0
	for q_u in q_nodes:
		sampled_nodes,L = find_sample(G,G_t,u,q_nodes,t_h)
		vec_u = f_v[q_u]
		edge_score = {}
		for v in sampled_nodes:
			vec_v = f_v[v]
			x = np.dot(vec_u,vec_v)
			score = sigmoid(x)
			p = calculate_probability(feat_b_ita, feat_b_ita_p, score) 
			edge_score[v] = p
		avg_prec = average_precision(G,edge_score,q_u)
		MAP+=(1.0/L)*avg_prec

	return MAP/len(q_nodes)
			
