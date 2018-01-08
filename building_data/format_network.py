

fs = open("network_algorithm_author_citation_www.txt")

edge_time  = {}

for line in fs:
	u,v,t = map(int,line.strip().split("\t"))
	print u,v,t
	edge = str(u)+","+str(v)
	if edge not in edge_time:
		edge_time[edge] = []
	edge_time[edge].append(t)

fs.close()

print "data loaded"


