// PointsFilter.cpp:激光点筛选类

#pragma once
#include "PointsFilter.h"
#include <iostream>
#include <direct.h>
#include <io.h> 
#include <fstream>
#include <iomanip>
#include <vector>
#include <string>
#include <stdio.h>
#include <tchar.h>

using namespace std;
using std::string;

class PointsFilter
{
	public:
		string in_path;
		string out_path;
		vector<string> SLAdata;
		double min_lon, max_lon, min_lat, max_lat, terrain_slope;
		int ac_level;

};

void SLApointsearch(string in_path, string out_path, vector<string> SLAdata, double min_lon, double max_lon, double min_lat, double max_lat, int ac_level, double terrain_slope);