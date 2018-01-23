#ifndef __METRICS_H_INCLUDED__
#define __METRICS_H_INCLUDED__
#include<map>
#include<vector>
#include<tuple>
#include "snap.h"

typedef std::vector<std::tuple<int,int,int> > vec_tup;

double avg_precision(vec_tup, PUNGraph, int, int, int);
double MAP(vec_tup, PUNGraph, std::vector<int>, int);

#endif
