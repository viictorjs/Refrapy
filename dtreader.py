# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 14:14:30 2019

@author: Riedel
"""

import matplotlib.pyplot as plt
import pygimli as pg
import pandas as pd
import numpy as np
import pathlib

def dtreader(path,profile):
    full_in_path=pathlib.Path(path)
    basepath=full_in_path.parents[0]
    file=pd.read_csv(path,delim_whitespace=True,header=None,names=['s_x','s_h','g_x','g_h','t'],error_bad_lines=False)
    #sanitize input data
    file=file.drop(file[file["t"]==0].index)
    file.reset_index(drop=True,inplace=True)
    #get out values too close to each other
    gxu=file.g_x.unique()
    sxu=file.s_x.unique()
    replacers=[]
    for i in gxu: 
        if np.min(np.abs(sxu-i)) >0 and  np.min(np.abs(sxu-i)) < 0.2:
            min_index=np.argmin(np.abs(sxu-i))
            print("yep", "gx: ",i," min  at index ", min_index, "value sx :", sxu[min_index])
            replacers.append([i,sxu[min_index]])
    #replace off shots with geophone positions
    #replace(toreplace,replacing)
    #replace(shots,geophone)
    for pair in replacers:
        file.replace(pair[1],pair[0],inplace=True)
    
    shots=file[['s_x','s_h']]
    shots=shots.rename(columns={'s_x':'g_x','s_h':'g_h'})
    geophones=file[['g_x','g_h']]
    t=file['t']*0.001 # file is in milliseconds
    
    #fuse
    geometry=pd.concat([shots,geophones])
    #drop duplicates
    geometry_single=geometry.drop_duplicates()
    geometry_single=geometry_single.sort_values('g_x')
    geometry_single=geometry_single.reset_index(drop=True)
    geometry_points=len(geometry_single)
    
    #https://stackoverflow.com/questions/37612366/index-of-matching-rows-in-pandas-dataframe-python
    
    #look up the tuple positions in the geometry table
    lookup_geoph=geophones.reset_index().merge(geometry_single.reset_index(), on=['g_x','g_h'])
    lookup_shots=shots.reset_index().merge(geometry_single.reset_index(), on=['g_x','g_h'])
    
    lookup_geoph=lookup_geoph.sort_values('index_x')
    lookup_shots=lookup_shots.sort_values('index_x')
    
    lookup_geoph.reset_index(drop=True,inplace=True)
    lookup_shots.reset_index(drop=True,inplace=True)
    #shots and geophones have same index_x-> integrity still there
    
    data=pd.concat([lookup_shots['index_y'], lookup_geoph['index_y'],t], axis=1, sort=False,ignore_index=True)
    data.columns=['s','g','t']
    # pygimli sgt  uses indexes starting at 1, we will turn this back later
    data['s']=data['s']+1
    data['g']=data['g']+1
    
    data=data.sort_values(['s','g','t'])
    
    
    #qc : We repack our files
    
    #make it negative heigths
    
    
    
    
    
# =============================================================================
    with open(pathlib.Path(basepath,profile+'.sgt'),mode='w+',newline='\n') as f:
        f.write(str(geometry_points)+ ' # shot/geophone points\n')
        f.write('#x y\n')
        geometry_single.to_csv(path_or_buf=f,sep=' ',header=False,index=False,line_terminator='\n')
        f.write('\n')
        f.write(str(len(data))+' # measurements\n')
        f.write('#s g t\n')
        data.to_csv(path_or_buf=f,sep=' ',header=False,index=False,line_terminator='\n')
# =============================================================================
        
        
    #stuff is written, we return to zeros
    data['s']=data['s']-1
    data['g']=data['g']-1
    
    
    #lets do some QC
    #get the shot positions back
    rec_shots=geometry_single.iloc[data['s'].values]
    rec_shots=rec_shots.rename(columns={'g_x':'s_x','g_h':'s_h'})
    rec_geophones=geometry_single.iloc[data['g'].values]
    rec_t=data['t']
    
    #reset their index, they are already in perfect order
    rec_shots.reset_index(drop=True, inplace=True)
    rec_geophones.reset_index(drop=True, inplace=True)
    rec_t.reset_index(drop=True, inplace=True)
    rebuilt=pd.concat([rec_shots,rec_geophones,rec_t],axis=1)
    
    
    #data=data.sort_values(['s','g'])
    return geometry_single,data