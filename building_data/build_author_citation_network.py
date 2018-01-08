import json
import pickle


if __name__=="__main__":

	ft = open("network_algorithm_author_citation_www.txt","w")
	fs = open("author_year_reference_www.json")
	for line in fs:
		data = json.loads(line)
		for i in xrange(len(data[u'author'])):
			for j in xrange(len(data[u'ref_author'])):
				ft.write(str(data[u'author'][i])+"\t"+str(data[u'ref_author'][j])+"\t"+str(data[u'year']))
				ft.write("\n")

	fs.close()
	ft.close()
