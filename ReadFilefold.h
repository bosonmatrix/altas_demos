// ReadFilefold.h������������ļ���Ŀ¼��ȡ��
// 
#pragma once

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


class ReadFilefold
{
	public:
		string path;
		vector<string>& files;
};

void getAllFiles(string path, vector<string>& files);

void getFiles(string path, vector<string>& files);

void getAllFilesName(string path, vector<string>& files);