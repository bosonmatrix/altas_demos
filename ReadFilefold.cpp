// ReadFilefold.cpp：激光点数据文件夹目录读取类

#include "ReadFilefold.h"

// 读取path目录里的所有txt文件
void getAllFiles(string path, vector<string>& files)
{  
	// 定义文件格式
	string type = "txt";
	string p;

	long hFile = 0;
	struct _finddata_t  fileInfo;

	if ((hFile = _findfirst(p.assign(path).append("\\*" + type).c_str(), &fileInfo)) != -1)
	{
		do
		{
			files.push_back(p.assign(path).append("\\").append(fileInfo.name));
		} while (_findnext(hFile, &fileInfo) == 0);
		_findclose(hFile);
	}
}


//读取path目录下的所有子文件夹
void getAllFilesName(string path, vector<string>& files)

{
	string p;

	intptr_t   hFile = 0;
	struct _finddata_t fileinfo;

	if ((hFile = _findfirst(p.assign(path).append("\\*").c_str(), &fileinfo)) != -1)
	{
		do
		{
			if ((fileinfo.attrib & _A_SUBDIR))
			{
				if (strcmp(fileinfo.name, ".") != 0 && strcmp(fileinfo.name, "..") != 0)
					files.push_back(p.assign(path).append("\\").append(fileinfo.name));
			}
		} while (_findnext(hFile, &fileinfo) == 0); 
		_findclose(hFile); 
	}

}

// 读取path目录里的所有文件（包括子文件夹）
void getFiles(string path, vector<string>& files)
{
	//文件句柄
	long   hFile = 0;
	//文件信息
	struct _finddata_t fileinfo;
	string p;
	if ((hFile = _findfirst(p.assign(path).append("\\*").c_str(), &fileinfo)) != -1)
	{
		do
		{
			if ((fileinfo.attrib & _A_SUBDIR))
			{
				if (strcmp(fileinfo.name, ".") != 0 && strcmp(fileinfo.name, "..") != 0)
					getFiles(p.assign(path).append("\\").append(fileinfo.name), files);
			}
			else
			{
				files.push_back(p.assign(path).append("\\").append(fileinfo.name));
			}
		} while (_findnext(hFile, &fileinfo) == 0);
		_findclose(hFile);
	}
}


