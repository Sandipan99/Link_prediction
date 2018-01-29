import tensorflow as tf
import numpy as np
import random
import graph as g
import math
import networkx as nx

def random_walk_neural_kernel(W, W_l, n, f_v, G):
	nodes = G.nodes()
	state_vector = tf.matmul(W,f_v)
	size = tf.shape(state_vector)
	for i in xrange(1,n):
		state_vector_intm = state_vector
		for i in xrange(len(nodes)):
			sum_ = 0.0
			v = nodes[i]
			for u in nx.all_neighbors(G,v):
				u_i = nodes.index(u)
				rho = tf.sigmoid(W_l,tf.concat([state_vector[u_i],f_v[i]]))
			 	sum_ += tf.multiply(tf.multiply(state_vector[u_i],rho),state_vector[i])
			state_vector_intm[i] = tf.add(state_vector_intm[i],state_vector[i])
		state_vector = state_vector_intm
	return state_vector, W, W_l

if __name__=="__main__":
	
	t_p = 24
	G = g.obtain_graph("text_file")
	f_v = g.obtain_node_features(G[t_p-1])

	p_s,n_s = g.find_pos_neg_samples(G)
		
	W = tf.Variable(tf.random_normal([dim,dim]))
	W_l = tf.Variable(tf.random_normal([dim,dim]))

	state_vector = random_walk_kernel(W, W_l, n, f_v, G[t_p-1])	
	loss = tf.reduce_mean(-math.log(tf.sigmoid(tf.multiply(state_vector[x_1],state_vector[x_2])))

