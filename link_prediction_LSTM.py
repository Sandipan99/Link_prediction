# input: graph
# output: accuracy of link prediction
# approach: (i) run W-L algorithm on the graph, (ii) represent each node by the label sequence of its and its neighbor's labels and input this sequence to the LSTM (node wise) (iii) learn representations of each label (iv) output of each LSTM is a vector which is a representation of the node (v) train for each existing edge as a positive example and non-edge as negative example...(vi)loss: logistic

import build_tree as bt
import tensorflow as tf
import numpy as np
import random
from tensorflow.contrib import rnn
            

def RNN(x, weights, biases,n_input,n_hidden):
    x = tf.reshape(x,[-1,n_input])
    x = tf.split(x,n_input,1)
    rnn_cell = rnn.BasicLSTMCell(n_hidden)

    outputs, states = rnn.static_rnn(rnn_cell, x, dtype=tf.float32)

    return tf.matmul(outputs[-1], weights['out'])+biases['out']


def obtain_positive_negative_sample(adj_matrix,label_tree):
    for i in xrange(len(adj_matrix)):
        for j in xrange(len(adj_matrix)):
            if adj_matrix[i][j]==1:
                x_p_u.append(label_tree[i])
                x_p_v.append(label_tree[j])
                y_p.append(1)
            else:    
                x_n_u.append(label_tree[i])
                x_n_v.append(label_tree[j])
                y_n.append(1)

    return x_p_u,x_p_v,y_p,x_n_u,x_n_v,y_n


if __name__=="__main":


    label_tree = bt.form_label_tree(adj_matrix,k)

    x_p_u,x_p_v,y_p,x_n_u,y_n_v = obtain_positive_negative_sample(adj_matrix,label_tree)


    n_input  = k+1
    n_hidden = 512
    training_iters = 20000
    display_step = 1000
    out_vector_dim = 100

    x = tf.placeholder("float",[None, n_input, 1])
    y = tf.placeholder("float",[None, vocab_size])

    weights_u = { 'out': tf.Variable(tf.random_normal([n_hidden, out_vector_dim]))}
    biases_u = {'out': tf.Variable(tf.random_normal([out_vector_dim]))}

    weights_v = { 'out': tf.Variable(tf.random_normal([n_hidden, out_vector_dim]))}
    biases_v = {'out': tf.Variable(tf.random_normal([out_vector_dim]))}


    pred = RNN(x, weights_u, biases_u, n_input, n_hidden)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred,labels=y))
    optimizer = tf.train.RMSPropOptimizer(learning_rate=0.001).minimize(cost)

    correct_pred = tf.equal(tf.argmax(pred,1), tf.argmax(y,1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred,tf.float32))
    init = tf.global_variables_initializer()

    with tf.Session() as session:
        session.run(init)
        step = 0
        offset = random.randint(0,n_input+1)
        end_offset = n_input + 1
        acc_total = 0
        loss_total = 0


        while step < training_iters:
            if offset > (len(training_data)-end_offset):
                offset = random.randint(0,n_input+1)
            symbols_in_keys = [ [dictionary[ str(training_data[i])]] for i in range(offset, offset+n_input)]
            symbols_in_keys = np.reshape(np.array(symbols_in_keys),[-1, n_input,1])

            symbols_out_onehot = np.zeros([vocab_size],dtype=float) 
            #print offset,n_input
            symbols_out_onehot[dictionary[str(training_data[offset+n_input])]]=1.0
            symbols_out_onehot = np.reshape(symbols_out_onehot,[1,-1])
            
            _, acc, loss, onehot_pred = session.run([optimizer, accuracy, cost, pred], feed_dict={x: symbols_in_keys, y: symbols_out_onehot})

            step += 1
            offset += (n_input+1)
            if step%display_step==0:
                print acc,loss,step
        print "optimization finished"
         


