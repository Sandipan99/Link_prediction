/*
implements link prediction in dynamic network by Katz 1953 both last and all time
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
#include<armadillo>

#include "Snap.h"


typedef std::vector<std::tuple<int,int,int> > vec_tup;

vec_tup pair_score_katz(PUNGraph G, std::vector<int> nodes, double beta){
	vec_tup pair_score;
	int u,v;
	std::map<int,int> node_id;
	std::map<int,int> id_node;
	std::vector<int>::iterator it;
	int cnt = 0;
	for(it=nodes.begin();it!=nodes.end();it++){
		node_id[cnt] = *it;
		id_node[*it] = cnt;
		cnt++;
	}
	int s = nodes.size();
	// creating the adjacency matrix...
	arma::mat adj_mat(s,s);
	for(int i=0;i<s-1;i++){
		for(int j=i+1;j<s;j++){
			u = node_id[i];
			v = node_id[j];
			if(G->IsEdge(u,v)){
				adj_mat(i,j)=1;
				adj_mat(j,i)=1;
			}
			else{
				adj_mat(i,j)=0;
				adj_mat(j,i)=0; 
			}
		}
	}
	// calculaing the katz score....
	int p_length = 5;
	beta*=beta;
	arma::mat adj_mat_mul = adj_mat * adj_mat;
	arma::mat score_mat = adj_mat_mul*beta;
	for(int i=3;i<p_length;i++){
		adj_mat_mul = adj_mat_mul * adj_mat;
		beta*=beta;
		score_mat = score_mat + adj_mat_mul*beta	
	}
	for(int i=0;i<s-1;i++){
		for(int j=i+1;j<s;j++){
			pair_score.push_back(std::make_tuple(node_id[i],node_id[j],score_mat(i,j)))
		}
	}
	return pair_score;

}

vec_tup predict_katz(PUNGraph G, int t){
	std::vector<int> all_pairs;
	int u,v;
	TUNGraph G_t = PUNGraph::New();
	if(s==0){
		TUNGraph::TNodeI NI;
		for(NI=G[t_p-1]->BegNI();NI!=G[t_p-1]->EndNI();NI++)
			all_pairs.push_back(NI.GetId());
		 return pair_score_katz(G[t_p-1],all_pairs);	
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
		return pair_score_katz(G_t,all_pairs);
	}

}


int main(int argc, char* argv[]){
	int u,v,t;
	int time_pred = 20;
	vec_tup predicted_set_last_katz, predicted_set_all_katz;
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

	predicted_set_last_katz = predict_katz(G,t_p);
	return 0;
}


