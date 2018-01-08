import json
import re
import pickle
import sys

def find_id(line):
	temp = line.strip().split("[")
	return int(temp[-1].replace("]",""))

def build_list(id_,paper_dict):
	x = id_%100
	if x not in paper_dict:
		paper_dict[x] = []
	paper_dict[x].append(id_)
	return paper_dict

		
if __name__=="__main__":
	paper_list = {}
	with open("author_year_reference_www.json","w") as ft:
		fs = open("world_wide_web_data.txt")
		for line in fs:
			if re.match("#index.*",line):
				reference = []
				reference_auth = []
				auth = []
				ind = int(line.strip().replace("#index",""))
				paper_list = build_list(ind,paper_list)
			if re.match("#@.*",line):
				temp = line.strip().split(",")
				for i in xrange(len(temp)):
					if len(temp[i])<=1:
						break
					try:
						auth.append(int(temp[i].split("[")[1].replace("]","")))
					except:
						print line
			if re.match("#y.*",line):
				try:
					year = int(line.strip().replace("#y",""))	
				except:
					year = 0
			
			if re.match("#%\*.*",line):
				reference.append(find_id(line))

			if re.match("#%@.*",line):
				temp = line.strip().split(",")
				print line
				if len(temp)>1:
					for i in xrange(len(temp)):
						if len(temp[i])<=1:
							break
						try:	
							reference_auth.append(int(temp[i].split("[")[1].replace("]","")))
						except:
							continue	
			if re.match("\n",line):
				print ind
				json.dump({'id':ind,'year':year,'author':auth,'reference':reference,'ref_author':reference_auth},ft)
				ft.write('\n')

		fs.close()

	ft = open("paper_list_www.pickle","w")
	pickle.dump(paper_list,ft)
	ft.close()		
