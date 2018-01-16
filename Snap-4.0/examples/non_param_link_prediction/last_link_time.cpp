/*

implements link prediction in dynamic network by Tylenda et. al. 2009
input: graph stream
output: predicted links
@author: Sandipan Sikdar
*/


#include<stdio.h>
#include<iostream>
#include<fstream>
#include<map>
#include<string>
#include<algorithm>
#include<vector>
#include<tuple>

#include "Snap.h"

typedef std::vector<std::tuple<int,int,int> > vec_tup;

int find_last_link_time(PUNGraph G[], int u, int v, int t){
	int i = t-1;
	int ll_t = 0;
	while(i>=0){
		ll_t++;
		if(G[i]->IsEdge(u,v))
			return ll_t;
		i--;
	}
	return t+1;
}


vec_tup predict_ll(PUNGraph G_t[], int t_p){
	vec_tup node_pairs;
	std::vector<int> node_list;
	TUNGraph::TNodeI NI;
	for(NI=G->BegNI();NI!=G->EndNI();NI++)
		node_list.push_back(NI.GetId());

	for(int i=0;i<node_list.size()-1;i++){
		for(int j=i+1;j<node_list.size();j++){
			node_pairs.push_back(std::make_tuple(u,v,find_last_link_time(G_t,u,v,t_p)))
		}
	}
	std::sort(begin(node_pairs), end(node_pairs), 
    	[](tuple<int, int, int> const &t1, tuple<int, int, int> const &t2) {
        return get<2>(t1) < get<2>(t2); 
    	}
	);
	return node_pairs;
}

int main (int argc, char* argv[]){

	int u,v,t;
	int time_pred = 20;
	vec_tup predicted_set_last;
	//std::map<std::string,std::vector<int> > link_time;
	PUNGraph G[24];
	//PUNGraph G_all = TUNGraph::New();
	for(int i=0;i<24;i++)
		G[i] = TUNGraph::New();
	std::ifstream in;
	in.open("network_algorithm_author_citation_www.txt");
	while(in >> u >> v >> t){
		if(t<1989)
			continue;
		else{	
			t = t-1989;
			//std::string e = std::to_string(u)+","+std::to_string(v);
			//link_time[e].push_back(t);
			if(!G[t]->IsNode(u))
				G[t]->AddNode(u);
			if(!G[t]->IsNode(v))
				G[t]->AddNode(v);
			if(!G[t]->IsEdge(u,v))
				G[t]->AddEdge(u,v);

			//combine all the graphs upto t
			/*
			if(!G_all->IsNode(u))
				G_all->AddNode(u);
			if(!G_all->IsNode(v))
				G_all->AddNode(v);
			if(!G_all->IsEdge(u,v))
				G_all->AddEdge(u,v);*/

		}
	}
	in.close();	

	predicted_set_last = predict_ll(G, time_pred);
	return 0;
}


