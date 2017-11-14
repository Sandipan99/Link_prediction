# implements Weisfeiler-Lehman algorithm used for isomorphism check
# input -> adjacency matrix
# output -> a list of labels with index representing node id

__author__ = "Sandipan Sikdar"

import sys

def compare(temp_1,temp_2):
	if temp_1[0] > temp_2[0]:
		return 1
	elif temp_1[0] < temp_2[0]:
		return 2
	else:
		l_1 = len(temp_1)
		l_2 = len(temp_2)
		for i in xrange(1,l_1):
			if i>l_2-1:
				return 1
			if temp_1[i]>temp_2[i]:
				return 1
			elif temp_1[i]<temp_2[i]:
				return 2
		if i<l_2-1:
			return 2
		else:
			return 0	

def sort_signature(uniq_sig):

	for i in xrange(len(uniq_sig)-1):
		for j in xrange(i+1,len(uniq_sig)):
			x = compare(uniq_sig[i],uniq_sig[j])
			if x==1:
				t = uniq_sig[i]
				uniq_sig[i] = uniq_sig[j]
				uniq_sig[j] = t
	return uniq_sig


def assign_label(node_sig,n_node):
	uniq_sig = []
	label = [0 for i in xrange(n_node)]
	for i in xrange(len(node_sig)):
		if node_sig[i] not in uniq_sig:
			uniq_sig.append(node_sig[i])	

	#print uniq_sig
	uniq_sig = sort_signature(uniq_sig)
	#print uniq_sig

	for i in xrange(len(node_sig)):
		label[i] = uniq_sig.index(node_sig[i])+1

	return label

	

def assign_sig(adj_mat,label,n_node):
	node_sig = []
	for i in xrange(n_node):
		temp = []
		#temp.append(label[i])
		for j in xrange(n_node):
			if (j!=i)and(adj_mat[i][j]==1):
				temp.append(label[j])
		temp.sort()
		temp.insert(0,label[i])
		node_sig.append(temp)
	return node_sig

def reached_convergence(label,new_label):
	for i in xrange(len(label)):
		if label[i]!=new_label[i]:
			return False
	return True

def obtain_label(adj_mat,n_node):	
	label = [1 for i in xrange(n_node)]
	
	node_sig = assign_sig(adj_mat,label,n_node)

	new_label = assign_label(node_sig,n_node)

	while not reached_convergence(label,new_label):
		label = new_label
		node_sig = assign_sig(adj_mat,label,n_node)
		new_label = assign_label(node_sig,n_node)

	return node_sig,label	

if __name__ == "__main__":
	#input in the form of adjacency list
	adj_mat = []
	fs = open(sys.argv[1])
	for line in fs:
		temp = map(int,line.strip().split(" "))
		adj_mat.append(temp)
	fs.close()

	n_node = len(temp)
	
	node_sig,label = obtain_label(adj_mat,n_node)

	print label
