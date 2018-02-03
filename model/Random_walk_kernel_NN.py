import networkx as nx
import tensorflow as tf
import numpy as np
import graph as g
import metrics
import random

def Random_walk_kernel_NN(G, W, decay, f_v, nodes, l, n):
        state_vector = {}
	for i in xrange(len(nodes)):
                v = nodes[i]
		state_vector[v] = tf.matmul(tf.reshape(f_v[i],[1,n]),W)
	l-=1
	while(l>0):
		state_vector_intm = state_vector
		for i in xrange(len(nodes)):
                        v = nodes[i]
			sum_ = tf.Variable(tf.zeros([n,1],tf.float64))
			for u in nx.all_neighbors(G,v):
				sum_ = tf.add(sum_,state_vector[u])
			state_vector_intm[v] = decay * tf.multiply(sum_,tf.matmul(tf.reshape(f_v[i],[1,n]),W))
		state_vector = state_vector_intm
		l-=1

	return state_vector

def positive(X,state_vector):
        print X[0]
        #Y = 2*state_vector[X[0]]
	return tf.log(tf.sigmoid(tf.tensordot(state_vector[X[0]],state_vector[X[1]],1)))

def negative(X,state_vector):
	score = 0.0
	for i in xrange(2,len(X)):
		score += tf.log(tf.sigmoid(-tf.tensordot(state_vector[X[0]],state_vector[X[i]],1)))
	return score/(len(X)-2)

def find_train_example(G_t,Q):
	nodes = G_t.nodes()
	random.shuffle(nodes)
        u = nodes[0]
	sample = [u]
	nbrs = []
	for v in nx.all_neighbors(G_t,u):
		nbrs.append(v)
        random.shuffle(nbrs)        
	sample.append(nbrs[0])
	for n in nodes:
		if n not in nbrs:
			if random.uniform(0,1)>0.5:
				sample.append(n)
				Q-=1
		if Q==0:
			break
	return tf.convert_to_tensor(sample)
		

if __name__=="__main__":

	Q = 5
        s = 10
	n = 5
	decay = 0.8
	l = 1
	G,G_t = g.obtain_graph_single("Data/Facebook/facebook_combined.txt",0.25)
        print "nodes in G ",len(G.nodes())
	f_v = g.obtain_features(G,n)
        f = tf.constant(f_v.real)
        #print f.dtype
	W = tf.Variable(tf.random_uniform([n,s],dtype=tf.float64)) #s is set by the user
        #print W.dtype
        #X = find_train_example(G_t,Q)
        
        X = tf.placeholder(tf.int32,[Q+2])
	nodes = G.nodes()
	state_vector = Random_walk_kernel_NN(G, W, decay, f, nodes, l, n)
    
	loss = - positive(X,state_vector) - Q*negative(X,state_vector)
	optimizer = tf.train.AdamOptimizer(0.0001).minimize(loss)	
	
	init = tf.global_variables_initializer()
	iterator = 1
	with tf.Session() as session:
		session.run(init)
		while iterator>0:
                        print "running for iteration", iterator
			_, cost, s_v = session.run([optimizer,loss,state_vector], feed_dict = {X:find_train_example(G,Q)})
			iterator-=1
                        print "iteration",iterator
		print "optimization complete - parameters obtained"
        '''  
		print metrics.evaluate(G,G_t,state_vector,t_h)

	'''
