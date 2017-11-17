#input: graph, labels (as output from W-L algorithm)
#output: label sequence representing each node...

import W_L_algorithm as wl

def form_label_tree(adj_matrix,k):

	n_node = len(adj_matrix)
	node_sig,label = wl.obtain_label(adj_matrix,n_node)

	node_neighbor = [[] for i in xrange(len(adj_matrix))]
	node_label = [[] for i in xrange(len(adj_matrix))]
	for i in xrange(len(adj_matrix)):
		for j in xrange(len(adj_matrix)):
			if adj_matrix[i][j]==1:
				node_neighbor[i].append(j)
	

	for i in xrange(len(node_neighbor)):
		temp = []
		node_label[i].append(i)
		j = k
		flag = 0
		for obj in node_neighbor[i]:
			temp.append(obj)
			node_label[i].append(obj)
			j-=1
		while j>0:
	
			for node in temp:
				for obj in node_neighbor[node]:
					if obj not in node_label[i]:
						node_label[i].append(obj)
						j-=1
						if j==0:
							flag = 1
							break
						temp.append(obj)
				if flag == 1:
					break
				temp.remove(node)
			if len(temp)==0:
				break
		for n in xrange(len(node_label[i])):
			node_label[i][n] = label[node_label[i][n]]

	return node_label 

if __name__=="__main__":
	adj_matrix = []
	fs = open("test_graph")
	for line in fs:
		temp = map(int,line.strip().split(" "))
		adj_matrix.append(temp)
	fs.close()
	k = 6
	label_tree = form_label_tree(adj_matrix,k)
	print label_tree

