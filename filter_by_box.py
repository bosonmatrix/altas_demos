import numpy as np
import os
from tqdm import tqdm

def read_cp_file(cp_file):
    with open(cp_file,encoding='utf-8') as f:
        cp=np.loadtxt(f,delimiter = '\t',skiprows=1)
    return cp

def filter_cp_file(cp_path,box):
    cp_dirs=os.listdir(cp_path)
    for cp_dir in cp_dirs:
        cp_sub_dir=cp_path+'/'+cp_dir+'/data/'
        cp_files=os.listdir(cp_sub_dir)
        for cp_file in tqdm(cp_files,desc='scanning files'):
            control_points=read_cp_file(cp_sub_dir+cp_file)
            if control_points.ndim==1:
                control_points=control_points.reshape(1,-1)
            if (box[0]<=control_points[:,1]).any() and (control_points[:,1]<=box[1]).any() and (box[2]<=control_points[:,2]).any() and (control_points[:,2]<=box[3]).any():
                print(cp_sub_dir+cp_file)

if __name__=='__main__':
    box=[116,119,36,39]
    cp_path=input('control point files\' path')
    filter_cp_file(cp_path,box)