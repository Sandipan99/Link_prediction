/*
implements link prediction in dynamic network by Liben-Nowell 2003, Adamic Adder 2003 both last and all time
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
#include<math.h>

#include "Snap.h"

typedef std::vector<std::tuple<int,int,double> > vec_tup;

TUNGraph::TNodeI nodepointer(PUNGraph G, int u){
	TUNGraph::TNodeI NI = G->BegNI();
	for(;NI<G->EndNI();NI++){
		if(NI.GetId()==u)
			return NI;
	}
}

std::vector<int> find_neighbors(PUNGraph G, int u){
	int v;
	std::vector<int> nbrs;
	std::vector<int>::iterator it;
	TUNGraph::TNodeI n_u;
	n_u = nodepointer(G,u);
	for(int e=0;e<NI.GetOutDeg();e++){
		v = NI.GetOutNId(e);
		nbrs.push_back(v);
	}
	return nbrs;
}

std::vector<int> find_intersection(std::vector<int> &a, std::vector<int> &b){
	std::sort(a.begin(),a.end());
	std::sort(b.begin(),b.end());
	std::vector<int> c;
	std::set_intersection(a.begin(),a.end(),b.begin(),b.end(),back_inserter(c));
	c.erase(std::unique(c.begin(), c.end()),c.end());
	return c;	
}

vec_tup pair_score_CN(PUNGraph G, std::vector<int> all_pairs){
	vec_tup pair_score;
	std::vector<int> int_node;
	double score;
	TUNGraph::TNodeI NI_u, NI_v;
	for(int i=0;i<all_pairs.size()-1;i++){
		for(int j=i+1;j<all_pairs.size();j++){
			u = all_pairs[i];
			v = all_pairs[j];
			int_node = find_intersection(find_neighbors(G,u),find_neighbors(G,v));
			score = int_node.size();
			pair_score.push_back(std::make_tuple(u,v,score));
			pair_score.push_back(std::make_tuple(v,u,score));

		}
	}
	return pair_score;
}

int calculate_AA_score(PUNGraph G, std::vector<int> node_list){
	TUNGraph::TNodeI NI;
	double sum = 0.0;
	for(int i=0;i<node_list.size();i++){
		NI = nodepointer(node_list[i]);
		sum+=1/log(NI.GetOutDeg());
	}
	return sum;
}

vec_tup pair_score_AA(PUNGraph G, std::vector<int> all_pairs){
	vec_tup pair_score;
	double score;
	std::vector<int> int_node;
	TUNGraph::TNodeI NI_u, NI_v;
	for(int i=0;i<all_pairs.size()-1;i++){
		for(int j=i+1;j<all_pairs.size();j++){
			u = all_pairs[i];
			v = all_pairs[j];
			int_node = find_intersection_set(find_neighbors(G,u),find_neighbors(G,v));
			score = calculate_AA_score(G,int_node);
			pair_score.push_back(std::make_tuple(u,v,score));
			pair_score.push_back(std::make_tuple(v,u,score));
		}
	}
	return pair_score;

}

vec_tup predict_CN(PUNGraph G[], int s, int t_p){
	std::vector<int> all_pairs;
	int u,v;
	TUNGraph G_t = PUNGraph::New();
	if(s==0){
		TUNGraph::TNodeI NI;
		for(NI=G[t_p-1]->BegNI();NI!=G[t_p-1]->EndNI();NI++)
			all_pairs.push_back(NI.GetId());
		 return pair_score_CN(G[t_p-1],all_pairs);	
	}
	else{	
		for(int i=0;i<t_p;i++){
			TUNGraph::TEdgeI EI;
			for(EI=G[i]->BegEI();EI!=G[i]->EndEI();EI++){
				u = EI.GetSrcNId();
				v = EI.GetDstNId();
				if(!G_t->IsNode(u)){
					G_t->AddNode(u);
					all_pairs.push_back(u);
				}	
				if(!G_t->IsNode(v)){
					G_t->AddNode(v);
					all_pairs.push_back(v);
				}
				if(!G_t->IsEdge(u,v))
					G_t->AddEdge(u,v);
			}
		}
		return pair_score_CN(G_t,all_pairs);
	}
	
}


vec_tup predict_AA(PUNGraph G[], int t_p, int s){
	std::vector<int> all_pairs;
	int u,v;
	TUNGraph G_t = PUNGraph::New();
	if(s==0){
		TUNGraph::TNodeI NI;
		for(NI=G[t_p-1]->BegNI();NI!=G[t_p-1]->EndNI();NI++)
			all_pairs.push_back(NI.GetId());
		 return pair_score_AA(G[t_p-1],all_pairs);	
	}
	else{	
		for(int i=0;i<t_p;i++){
			TUNGraph::TEdgeI EI;
			for(EI=G[i]->BegEI();EI!=G[i]->EndEI();EI++){
				u = EI.GetSrcNId();
				v = EI.GetDstNId();
				if(!G_t->IsNode(u)){
					G_t->AddNode(u);
					all_pairs.push_back(u);
				}	
				if(!G_t->IsNode(v)){
					G_t->AddNode(v);
					all_pairs.push_back(v);
				}
				if(!G_t->IsEdge(u,v))
					G_t->AddEdge(u,v);
			}
		}
		return pair_score_AA(G_t,all_pairs);
	}
	
}

int main(int argc, char *argv[]){
	
	int u,v,t;
	int time_pred = 20;
	vec_tup predicted_set_last_AA, predicted_set_all_AA, predicted_set_last_CN, predicted_set_all_CN;
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


		}
	}
	in.close();	

	predicted_set_last_CN = predict_CN(G, time_pred, 0);
	predicted_set_all_CN = predict_CN(G, time_pred, 1);
	return 0;
}

