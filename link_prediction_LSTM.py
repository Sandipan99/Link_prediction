# input: graph
# output: accuracy of link prediction
# approach: (i) run W-L algorithm on the graph, (ii) represent each node by the label sequence of its and its neighbor's labels and input this sequence to the LSTM (node wise) (iii) learn representations of each label (iv) output of each LSTM is a vector which is a representation of the node (v) train for each existing edge as a positive example and non-edge as negative example...(vi)loss: logistic

import build_tree as bt

