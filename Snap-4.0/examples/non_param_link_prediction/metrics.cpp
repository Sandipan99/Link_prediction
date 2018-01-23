#include "metrics.h"
#include<bits/stdc++.h>


double avg_precision(vec_tup T, PUNGraph G, int u, int flag, int L){ // flag=0 gives ascending order, flag>0 gives descending order 
	std::vector<std::pair<double,int> > node_score;
	double score;
	int v;
	for(i=0;i<T.size();i++){
		score = std::get<2>(T[i]);
		v = std::get<1>(T[i]);
		if(std::get<0>(T[i])==u)
			if(flag==0)
				score = 1/score;
			node_score.push_back(std::make_pair(score,v));
	}
	sort(node_score.begin());

	double sum = 0.0;
	int cnt = 0, p_cnt = 0;
	for(int i=0;i<node_score.size();i++){
		cnt++;
		v = node_score[i].second;
		if(G->IsEdge(u,v)){
			p_cnt++;
			sum+= (double)(p_cnt)/cnt;
		}
	}
	return sum/L;	

}

double MAP(vec_tup T, PUNGraph G, std::vector<int> all_nodes, int s_t){
	int u;
	double sum = 0.0;
	std::vector<int>::iterator it;
	for(it = all_nodes.begin();it!=all_nodes.end();it++){
		u = *it;
		sum+=avg_precision(T,G,u,s_t,L);
	}
	return sum/all_nodes.size();
}

