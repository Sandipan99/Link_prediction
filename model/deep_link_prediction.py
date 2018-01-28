import tensorflow as tf
import numpy as np
import random
import graph as g
import math

def random_walk_kernel(W, W_l, n, f_v, G):
	state_vector = tf.matmul(W,f_v)
	size = tf.shape(state_vector)
	for i in xrange(1,n):
		state_vector_intm = state_vector
		for j in xrange(size[0]):
			sum_ = 0.0
			v = size[0]
			for u in nbr[v]:
				rho = tf.sigmoid(W_l,tf.concat([state_vector[u],f_v[v]]))
			 	sum_ += tf.multiply(tf.multiply(state_vector[u],rho),state_vector[v])
			state_vector_intm[v] = tf.add(state_vector_intm[v],state_vector[v])
		state_vector = state_vector_intm
	return state_vector, W, W_l

if __name__=="__main__":
	
	G = g.obtain_graph("text_file")
	f_v = g.obtain_node_features(G)
	#nbr = g.find_neighbor(G)

	p_s,n_s = g.find_pos_neg_samples(G)
		
	W = tf.Variable(tf.random_normal([dim,dim]))
	W_l = tf.Variable(tf.random_normal([dim,dim]))

	state_vector = random_walk_kernel(W, W_l, n, f_v, G)	
	loss = tf.reduce_mean(-math.log(tf.sigmoid(tf.multiply(state_vector[x_1],state_vector[x_2])))

