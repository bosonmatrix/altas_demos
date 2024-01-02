// PointsFilter.cpp:�����ɸѡ��

#include "PointsFilter.h"

void SLApointsearch(string in_path, string out_path, vector<string> SLAdata, double min_lon, double max_lon, double min_lat, double max_lat, int ac_level, double terrain_slope)
{
	// ����ļ�����ǰ׺
	string PREFIX = "\\output_";
	//���һ�����ܵ�txt����total_rows����
	ofstream total_out;
	string totalout_path = out_path;
	totalout_path.append("\\total.txt");
	total_out.open(totalout_path);
	if (!total_out.is_open())
	{
		cout << "Error opening total.txt" << endl; 
		exit(1);
	}
	total_out << "0\t\t\t\t" << endl;
	int total_rows = 0;


	for (size_t i = 0; i < SLAdata.size(); i++)
	{
		cout << SLAdata[i].c_str() << endl;
		// ��һ��txt�ļ�
		ifstream infile;
		infile.open(SLAdata[i].c_str());
		if (!infile.is_open())
		{
			cout << "Error opening file" << SLAdata[i].c_str() << endl; 
			exit(1);
		}

		// ��ȡ���txt���ļ���
		size_t datapath_len = in_path.length();
		string outfile_name = SLAdata[i].erase(0, datapath_len + 1);
		string outfile_path = "";
		outfile_path.append(out_path);
		outfile_path.append(PREFIX);
		outfile_path.append(outfile_name);

		// �����txt�ļ�
		ofstream outfile(outfile_path);
		if (!outfile.is_open())
		{
			cout << "Error writing file" << outfile_path; 
			exit(1);
		}
		// ��һ��������
		outfile << "0\t\t\t\t" << endl;
		// ׼��ɸѡ
		double buffer[6];
		int out_rows = 0;
		string temp;
		//infile�ļ�ͷ����
		getline(infile, temp);

		while (!infile.eof())
		{
			infile >> buffer[0] >> buffer[1] >> buffer[2] >> buffer[3] >> buffer[4] >> buffer[5];
			if (buffer[1] > min_lon && buffer[1] <max_lon && buffer[2]>min_lat && buffer[2] < max_lat && buffer[4] < ac_level && abs(buffer[5]) < terrain_slope)
			{
				out_rows++;
				total_rows++;
				outfile.setf(ios::fixed);
				outfile << out_rows << "\t";
				outfile << fixed << setprecision(6) << buffer[1] << "\t" << buffer[2] << "\t";
				outfile << fixed << setprecision(3) << buffer[3] << "\t";
				outfile << fixed << setprecision(0) << buffer[4] << "\t";
				outfile << fixed << setprecision(6) << buffer[5] << endl;

				total_out.setf(ios::fixed);
				total_out << total_rows << "\t";
				total_out << fixed << setprecision(6) << buffer[1] << "\t" << buffer[2] << "\t";
				total_out << fixed << setprecision(3) << buffer[3] << "\t";
				total_out << fixed << setprecision(0) << buffer[4] << "\t";
				total_out << fixed << setprecision(6) << buffer[5] << endl;
			}
		}
		outfile.seekp(ios::beg);
		// �ļ�ָ��ص���ͷ��д�����
		outfile << out_rows;

		infile.close();
		outfile.close();

		// �Ƴ�����������Ҫ�ĵ�Ŀ��ļ�
		if (out_rows == 0)
		{
			remove(outfile_path.c_str());
		}

		outfile_name.clear();
		outfile_path.clear();
	}

	total_out.seekp(ios::beg);
	// �ļ�ָ��ص���ͷ��д�����
	total_out << total_rows;
	total_out.close();
}
