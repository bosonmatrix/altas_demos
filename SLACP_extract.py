import numpy as np
import pandas as pd
# from scipy.spatial import KDTree
from sklearn import neighbors
import matplotlib.pyplot as plt 
import pyproj
import os
from tqdm import tqdm
import time
import warnings
 
warnings.filterwarnings('ignore')

def read_cp_file(cp_file):
    '''
    load control points file
    input:
    cp_file: the control point file
    output:
    cp: control points in dataframe format, [index	longitute	lattitute	level	height level	terrain slope]
    '''
    cp = pd.read_csv(cp_file, sep='\t', header=0)
    return cp

def read_bp_file(bp_file):
    '''
    load base points file
    input:
    bp_file: base point file
    output:
    bp_digital: control points in dataframe format [longitute	lattitute	level]
    '''
    with open(bp_file,'r') as f:
        bp=f.read()
        bp_list=bp.split('\n')
        bp_digital=[each.split('  ') for each in bp_list[3:-1]]
        bp_digital=np.array([list(filter(None,each)) for each in bp_digital])
        bp_digital=bp_digital.astype('float')
    return bp_digital[:,1:5]

def numbering(points):
    ids=[]
    for point in points:
        if (-30<point[1]<60 and 27<point[0]<59.5) or (-10<point[1]<60 and 59.5<point[0]<80):
            ids.append(1)
        elif(-30<point[1]<60 and -50<point[0]<27):
            ids.append(2)
        elif(0<point[1]<80 and 60<point[0]<180) or (59.5<point[1]<80 and -180<point[0]<-170):
            ids.append(3)
        elif(-50<point[1]<0 and 60<point[0]<180):
            ids.append(4)
        elif(0<point[1]<59.5 and -180<point[0]<-30) or (59.5<point[1]<80 and -180<point[0]<-60):
            ids.append(5)
        elif(-50<point[1]<0 and -180<point[0]<-30):
            ids.append(6)
        elif(-50<point[1]<0 and 0<point[0]<110):
            ids.append(7)
        elif(-79<point[1]<-50 and 110<point[0]<180):
            ids.append(8)
        elif(-79<point[1]<-50 and -180<point[0]<-90):
            ids.append(9)
        elif(-79<point[1]<-50 and -90<point[0]<0):
            ids.append(10)
        elif(59.5<point[1]<80 and -10<point[0]<-60):
            ids.append(11)
    return set(ids)

def extract_in_loop(cp_path,geosrs,prosrs,level_threshold,slope_threshold,base_points_arr=None,box=None,search_type=None,search_range=None):
    '''
    extracting adjacent points in iterations
    input:
    bp_file: base point(center of the circle) file
    cp_path: control point file
    geosrs: geolocation refrence system
    prosrs: projection refrence system
    level_threshold: the altimetry accuracy threshold, control point that is HIGHER than this will be excluded
    slope_threshold: the slope threshold, control point whose slope is HIGHER than this will be excluded
    search_type: 'range': search by range, 'amount': search by amount of adjacent points
    search_range: search range, in meter
    search_amount: amount of adjacent points
    output:
    nearby_cp_filtered: extracted adjacent points, further filtered under slope threshold and accuracy threshold
    '''
    filtered_indices=[]
    # nearby_cp_filtered = pd.DataFrame(data=None,columns=['longitute','latitute','level','height level','terrain slope'])
    # nearby_cp_filtered=np.array((len(base_points_arr)))
    cp_dirs=os.listdir(cp_path)

    if search_type=='adjacent':
        base_points=pd.DataFrame(base_points_arr,columns=['pointID','lon','lat','level'])
        p1 = pyproj.Proj(init=geosrs)
        p2 = pyproj.Proj(init=prosrs)
        xprj, yprj = pyproj.transform(p1, p2,x=base_points['lon'],y=base_points['lat'])
        tqdm.write('base points are projected')
        time.sleep(0.1)
        base_points['lon_prjd']=xprj
        base_points['lat_prjd']=yprj
        
        nearby_cp_filtered = pd.DataFrame(columns=['bp_index', 'nearby_cp'])
        
        for index in tqdm(range(base_points.shape[0]),desc='extracting adjacent control points'):
            tqdm.write(f'processing the {index+1}th base point...')
            time.sleep(0.1)
            nearby_cp_tmp=np.empty(shape=[0,4])
            for cp_dir in cp_dirs:
                if os.path.isdir(cp_path+cp_dir):
                    cp_sub_dir=cp_path+cp_dir+'/data/'
                    tmp_split=str.split(cp_dir,sep='_')
                    if eval(tmp_split[0]) in numbering([base_points.loc[index,['lon','lat']].values]):
                        cp_files=os.listdir(cp_sub_dir)
                        for cp_file in cp_files:
                            tqdm.write(f'searching in the control point file {cp_file}...')
                            time.sleep(0.1)
                            control_points=read_cp_file(cp_sub_dir+cp_file)
                            if control_points['lon'].min()<base_points.loc[index,'lon']<control_points['lon'].max() and control_points['lat'].min()<base_points.loc[index,'lat']<control_points['lat'].max():
                                xprj, yprj = pyproj.transform(p1, p2,x=control_points['lon'],y=control_points['lat'])
                                control_points['lon_prjd']=xprj
                                control_points['lat_prjd']=yprj
                                control_points_tree=neighbors.KDTree(control_points[['lon_prjd','lat_prjd']].values)
                                filtered_indices=[]
                                nearby_cp_indices=control_points_tree.query_radius(base_points.loc[index,['lon_prjd','lat_prjd']].values.reshape(1,-1),r=search_range)
                                nearby_cp_indices=np.concatenate(nearby_cp_indices)
                                for index_ in nearby_cp_indices:
                                    if control_points.iloc[index_,4]<=level_threshold and np.fabs(control_points.iloc[index_,5])<=slope_threshold:
                                        filtered_indices.append(index_)
                                if len(filtered_indices)!=0:
                                    nearby_cp_tmp=np.vstack(control_points.iloc[filtered_indices,1:-3].values)
                                nearby_cp_filtered.loc[len(nearby_cp_filtered),['bp_index','nearby_cp']]=[index,nearby_cp_tmp]
    elif search_type=='box':
        nearby_cp_filtered=pd.DataFrame(columns=['n','lon','lat','h_interp','ac_level','terrain_slope'])
        for cp_dir in cp_dirs:
            if os.path.isdir(cp_path+cp_dir):
                cp_sub_dir=cp_path+cp_dir+'/data/'
                tmp_split=str.split(cp_dir,sep='_')
                tmp_points=np.array([[box[0],box[1]],[box[2],box[3]]])
                if eval(tmp_split[0]) in numbering(tmp_points):
                    cp_files=os.listdir(cp_sub_dir)
                    for cp_file in cp_files:
                        tqdm.write(f'searching in the control point file {cp_file}...')
                        time.sleep(0.1)
                        control_points=read_cp_file(cp_sub_dir+cp_file)
                        # if (control_points['lon'].min()<box[0]<control_points['lon'].max() and control_points['lat'].min()<box[1]<control_points['lat'].max()) or\
                        #     (control_points['lon'].min()<box[2]<control_points['lon'].max() and control_points['lat'].min()<box[3]<control_points['lat'].max()):
                        indices=(box[0]<=control_points['lon']) & (control_points['lon']<=box[2]) & \
                        (box[1]<=control_points['lat']) & (control_points['lat']<=box[3]) & \
                        (control_points['ac_level']<=level_threshold) & \
                        (control_points['terrain_slope'] <= slope_threshold)
                        nearby_cp_filtered=pd.concat([nearby_cp_filtered,control_points[indices]],axis=0)
    return nearby_cp_filtered

def output_cps(base_points,nearby_cp,output_file,output_type=None,method_type=None):
    if output_type=="SAR":
        if method_type=='adjacent':
            with open(output_file,'w+') as f:
                amount=len(base_points)
                f.write(str(amount)+'\n')
                for index in tqdm(range(amount),desc='writing to file'):
                    f.write('Begin\t%s\t%.4f\t%.4f\t%.4f\n' %(str(base_points[index,0]),base_points[index,0],base_points[index,1],base_points[index,2]))
                    nearby_cp_tmp=nearby_cp.loc[index,'nearby_cp']
                    for each in nearby_cp_tmp:
                        f.write('%.4f\t%.4f\t%.4f\n' %(each[0],each[1],each[2]))
                    f.write('End\n')   
                    f.write('\n')
        elif method_type=='box':
            np.savetxt(output_file, nearby_cp, header='n lon lat h_interp ac_level terrain_slope', comments='', delimiter='\t', fmt='%d %f %f %f %d %f')
    elif output_type=='XQsoftware':
        with open(output_file) as f:
            pass

if __name__=='__main__':
    bp_file=r'E:/phD_career/活儿/173/data/base_points/ObjResidual.txt'
    SLACP_path=r'E:/phD_career/活儿/173/data/ATLAS/2020/'
    output_file=r'E:/phD_career/活儿/173/data/base_points/ObjResidual_adjacent_cps.txt'
    
    geosrs="epsg:4326"
    prosrs="epsg:32651"
    level_threshold=3
    slope_threshold=0.1
    search_type='box'
    search_range=500#5e5
    box=[117,37,119,45]

    base_points_arr=read_bp_file(bp_file)
    extracted_points=extract_in_loop(SLACP_path,geosrs,prosrs,level_threshold,slope_threshold,base_points_arr=None,box=box,search_type=search_type,search_range=search_range)
    # with open('nearby_cp_filtered_t.txt', 'r') as file:
    #     content = file.read()
    # # extracted_points_str = eval(content)
    # extracted_points = []
    # for sublist in content:
    #     numbers = [float(elem) for elem in sublist]
    #     extracted_points.append(numbers)
    output_cps(base_points_arr,extracted_points,output_file,output_type='SAR',method_type='box')

    tqdm.write('done')