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

public class feat_mat{
	std::map<std::string,int> all_pair_feat;
	std::map<std::string,int> edge_convert;

	public:
	void insert_a_p_f(std::string s){
		if(all_pair_feat.find(s) == all_pair_feat.end())
			all_pair_feat[s] = 1;
		else	all_pair_feat[s]++;
	}

	void insert_e_c(std::string s){
		if(edge_convert.find(s) == edge_convert.end())
			edge_convert[s] = 1;
		else	edge_convert[s]++;
	}

	int find_a_p_f(std::string s){
		if(all_pair_feat.find(s)==all_pair_feat.end())
			return 0;
		else	return all_pair_feat[s];
	}

	int find_edge_convert(std::string s){
		if(edge_convert.find(s)==edge_convert.end())
			return 0;
		else	return edge_convert[s];
	}

		
};

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

std::vector<int> create_node_list(PUNGraph G[], int t, int p){
	std::vector<int> nodes;
	TUNGraph::TNodeI NI;
	for(int i=p;i<=t,i++){
		 for(NI=G[i]->BegNI();NI!=G[i]->EndNI();NI++)
			nodes.push_back(NI.GetId());
	}
	nodes.erase(std::unique(nodes.begin(),nodes.end()),nodes.end());
	return nodes;
}

int find_last_link_time(PUNGraph G[], int u, int v, int t){
	int i = t-1;
	int ll_t = 0;
	while(i>=0){
		ll_t++;
		if(G[i]->IsEdge(u,v))
			return ll_t;
		i--;
	}
	return 0;
}

double TV_distance(std::vector<double> X, std::vector<double> Y){
	double sum = 0.0;
	for(int i=0;i<(int)X.size();i++){
		sum+=fabs(X[i]-Y[i]);
	}
	sum/=2;
	return sum;
}


double prediction(PUNGraph G[], int p, int t_p){
	//obtain node set...includes all nodes that appeared at least once till (t_predict-1)
	int u,v,s_cnt,s_llt;
	feat_mat G_s[t_p+1];
	std::vector<int> node_list, nbrs_u, nbrs_v;
	std::string f_str;	
	//create feaure matrix for edges... 
	for(int i=1;i<t_p;i++){  
		TUNGraph::TNodeI NI;
		for(NI=G[i]->BegNI();NI!=G[i]->EndNI();NI++)
			node_list.push_back(NI.GetId());	
		for(j=0;j<node_list.size()-1;j++){
			for(k=j+1;k<node_list.size();k++){
				u = node_list[j];
				v = node_list[k];
				nbrs_u = find_neighbors_over_time(G[i],u,p,t_p);
				nbrs_v = find_neighbors_over_time(G[i],v,p,t_p);
				s_cnt = find_intersection(nbrs_u,nbrs_v);
				s_llt = find_last_link_time(G,u,v,i);
				f_str = std::to_string(s_cnt)+","+std::to_string(s_llt);
				G_s[i].insert_a_p_f(f_str);
				if(G[i]->IsEdge(u,v))
					G_s[i].insert_e_c(f_str);
			}
		}
		node_list.clear();
	}
	//predict edges.....
	node_list_t = create_node_list(G,time_pred-1);
	for(int i=0;i<(int)node_list_t.size()-1;i++){
		for(int j=i;j<(int)node_list_t.size();j++){
			u = node_list_t[i];
			v = node_list_t[j];
			nbrs_u = find_neighbors_over_time(G[i],u,p,t_p);
			nbrs_v = find_neighbors_over_time(G[i],v,p,t_p);
			s_cnt = find_intersection(nbrs_u,nbrs_v);
			s_llt = find_last_link_time(G,u,v,i);
			f_str = std::to_string(s_cnt)+","+std::to_string(s_llt);
		}
	}	 
}

int main (int argc, char* argv[]){

	int u,v,t;
	int time_pred = 20;
	//std::map<std::string,std::vector<int> > link_time;
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
			if(!G[t]->IsNode(u))
				G[t]->AddNode(u);
			if(!G[t]->IsNode(v))
				G[t]->AddNode(v);
			if(!G[t]->IsEdge(u,v))
				G[t]->AddEdge(u,v);
		}
	}
	in.close();
	predict(G,p,t_p);	
	return 0;
}


