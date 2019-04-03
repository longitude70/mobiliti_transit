#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 16:11:12 2019

@author: colinlaurence
"""
import geopandas as gp
import pandas as pd
import numpy as np
import fiona
import shapely
import datetime as dt
import matplotlib as plt
#import cartopy
import pyproj
from scipy.spatial import distance

stops_df = pd.read_csv("vta_gtfs/stops.txt",header=0)
nodes_df = pd.read_csv("mobiliti_data/nodes_s_c.csv",header=0)
#print(stops_df.head(3))
#print(nodes_df.x.head(3))
#print(nodes_df.y.head(3))
node_lat=nodes_df.lat[0]
node_lon=nodes_df.lng[0]
#print(node_lat)
def wgs2utm(row):
    myProj = pyproj.Proj("+proj=utm +zone=10S, +south +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
    return myProj(row['lng'], row['lat'], inverse=False)
    


nodes_df['xy']= nodes_df.apply(wgs2utm,axis=1)

#print(nodes_df.xy.head(3))
stops_df.rename(columns={'stop_lat':'lat', 'stop_lon':'lng'}, inplace=True)
stops_df['xy']= stops_df.apply(wgs2utm,axis=1)
#print(stops_df.xy.head(3))

"""def closest_node(node):#jaime from stackoverflow
    nodes = np.asarray((nodes_df['xy']))
    node = np.asarray(node['xy'])
    dist = np.linalg.norm(nodes-node)
    return np.argmin(dist)"""

def closest_node(node):
    nodes = np.asarray((nodes_df['xy']))
    node=np.asarray(node['xy'])
    closest_index = distance.cdist([node], nodes).argmin()
    return nodes[closest_index]

stops_df['node']= stops_df.head(10).apply(closest_node,axis=1)
print(stops_df['node'].head(20))
