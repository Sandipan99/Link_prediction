// implements the non parametric link prediction in dynamic network alogrithm proposed by P. Sarkar et. al. in ICML 2012
// input: graph stream
// output: predicted links


#include<stdio.h>
#include<iostream>
#include<fstream>
#include<map>
#include<string>
#include<algorithm>
#include<vector>
#include "Snap.h"


TUNGraph::TNodeI nodepointer(PUNGraph G, int u){
	TUNGraph::TNodeI NI = G->BegNI();
	for(;NI<G->EndNI();NI++){
		if(NI.GetId()==u)
			return NI;
	}
}

std::vector<int> find_neighbors(PUNGraph G, int u){
	int v;
	std::vector<int> nbrs_1;
	std::vector<int>::iterator it;
	TUNGraph::TNodeI n_u;
	n_u = nodepointer(G,u);
	for(int e=0;e<NI.GetOutDeg();e++){
		v = NI.GetOutNId(e);
		nbrs_1.push_back(v);
	}
	std::vectors<int> nbrs_2;
	for(it=nbrs.begin();it!=nbrs.end();it++){
		n_u = nodepointer(G,*it);
		for(int e=0;e<NI.GetOutDeg();e++){
			v = NI.GetOutNId(e);
			nbrs_2.push_back(v);
		}
	}
	std::vector<int> nbrs = nbrs_1;
	nbrs.insert(nbrs.end(),nbrs_2.begin(),nbrs_2.end());
	return nbrs;
}

std::vector<int> find_neighbors_over_time(PUNGraph G[], int u, int p, int t_p){
	std::vector<int> lst_ret;
	std::vector<int> lst_final;
	int x = 0;
	while(x<p){
		lst_ret = find_neighbors(G[t_p-x],u);
		lst_final.insert(lst_final.end(),lst_ret.begin(),lst_ret.end());
		x--;
	}
	return lst_final;
}

int find_intersection(std::vector<int> &a, std::vector<int> &b){
	std::sort(a.begin(),a.end());
	std::sort(b.begin(),b.end());
	std::vector<int> c;
	std::set_intersection(a.begin(),a.end(),b.begin(),b.end(),back_inserter(c));
	c.erase(std::unique(c.begin(), c.end()),c.end());
	return c.size();	
}

int count_common_neighbors(PUNGraph G[], int u, int v, int p, int t_p){  //counts the number of common neighbors between u and v, neighborhood includes 2-hop neighbors of last p time steps
	std::vector<int> nbr_u;
	std::vector<int> nbr_v;
	nbr_u = find_neighbors_over_time(G,u,p,t_p);
	nbr_v = find_neighbors_over_time(G,v,p,t_p);
	return find_intersection(nbr_u,nbr_v);	
}


int main (int argc, char* argv[]){

	int u,v,t;
	int time_of_prediction = 20;
	std::map<std::string,std::vector<int>> link_time;
	PUNGraph G[24];
	for(int i=0;i<24;i++)
		G[i] = TUNGraph::New();
	std::ifstream in;
	in.open("network_algorithm_author_citation_www.txt");
	while(in >> u >> v >> t){
		if(t<1989)
			continue;
		else{	
			t = t-1989;
			std::string e = std::to_string(u)+","+std::to_string(v);
			link_time[e].push_back(t);
			if(!G[t]->IsNode(u))
				G[t]->AddNode(u);
			if(!G[t]->IsNode(v))
				G[t]->AddNode(v);
			if(!G[t]->IsEdge(u,v))
				G[t]->AddEdge(u,v);
		}
	}
	in.close();
	return 0;
}


