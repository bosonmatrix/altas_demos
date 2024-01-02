// ReadFilefold.cpp������������ļ���Ŀ¼��ȡ��

#include "ReadFilefold.h"

// ��ȡpathĿ¼�������txt�ļ�
void getAllFiles(string path, vector<string>& files)
{  
	// �����ļ���ʽ
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


//��ȡpathĿ¼�µ��������ļ���
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

// ��ȡpathĿ¼��������ļ����������ļ��У�
void getFiles(string path, vector<string>& files)
{
	//�ļ����
	long   hFile = 0;
	//�ļ���Ϣ
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


