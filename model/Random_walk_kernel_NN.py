import networkx as nx
import tensorflow as tf
import numpy as np
import garph as g
import metrics
import random

def Random_walk_kernel_NN(G, W, decay, f_v, nodes, l):
	state_vector = {}
	for v in nodes:
		state_vector[v] = tf.matmul(f_v[v],W)
	l-=1
	while(l>0):
		state_vector_intm = state_vector
		for v in nodes:
			sum_ = tf.Variable(tf.zeros([len(f_v[v])],tf.float32))
			for u in nx.all_neighbors(G,v):
				sum_ = tf.add(sum_,state_vector[u])
			state_vector_intm[v] = decay * tf.multiply(sum_,tf.matmul(f_v[v],W))
		state_vector = state_vector_intm
		l-=1

	return state_vector

def positive(X,state_vector):
	return tf.log(tf.sigmoid(tf.dot(state_vector[X[0]],state_vector[X[1]])))

def negative(X,state_vector):
	score = 0.0
	for i in xrange(2,len(X)):
		score += tf.log(tf.sigmoid(-tf.dot(state_vector[X[0]],state_vector[X[i]])))
	return score/(len(X)-2)

def find_train_example(G_t,Q):
	nodes = G_t.nodes()
	u = random.shuffle(nodes)[0]
	sample = [u]
	nbrs = []
	for v in nx.all_meighbors(G_t,u):
		nbrs.append(v)
	sample.append(random.shuffle(nbrs)[0])
	for n in nodes:
		if n not in nbrs:
			if random.uniform(0,1)>0.5:
				sample.append(n)
				Q-=1
		if Q==0:
			break
	return sample
		

if __name__=="__main__":

	Q = 5
	n = 5
	decay = 0.8
	l = 4
	G,G_t = g.obtain_graph_single("Data/Facebook/facebook_combined.txt",0.25)
	f_v = g.obtain_node_features(G_t,n)
	W = tf.Variable(tf.random_normal([n,s])) #s is set by the user
	nodes = G_t.nodes()
	state_vector = Random-walk_kernel_NN(G_t, W, decay, f_v, nodes, l)
	loss = - positive(X,state_vector) - Q*negative(X,state_vector)
	optimizer = tf.train.AdamOptimizer(0.0001).minimize(loss)	
	
	init = tf.global_variables_initializer()
	iterator = 50000
	with tf.Session() as session:
		session.run(init)
		while iterator>0:
			_, cost, s_v = session.run([optimizer,loss,state_vector], feed_dict = {X:find_train_example(G_t,Q)})
			iterator-=1
		print "optimization complete - parameters obtained"

		print metrics.evaluate(G,G_t,state_vector,t_h)

	
