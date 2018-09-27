#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 20:54:36 2018

@author: Mark
"""

import os
import requests
import tempfile

import geopandas as gpd
import networkx as nx
import osmnx as ox
import numpy as np
import peartree as pt
from shapely.geometry import Point


def main():
    # tl_query = 'https://transit.land/api/v1/feeds?bbox=-73.97339,40.649778,-73.946532,40.670353'
    
    # resp = requests.get(tl_query)
    # rj = resp.json()
    
    # zip_url = None
    # for f in rj['feeds']:
    #     if 'brooklyn' in f['onestop_id']:
    #         zip_url = f['url']
            
    # td = tempfile.mkdtemp()
    # path = os.path.join(td, 'mta_bk.zip')
    
    # resp = requests.get(zip_url)
    # open(path, 'wb').write(resp.content)

    
    feed = pt.get_representative_feed('reduced_stops/updatedv1.zip')
    
    start = 7*60*60  # 7:00 AM
    end = 10*60*60  # 10:00 AM
    
    G = pt.load_feed_as_graph(feed, start, end)
    pt.generate_plot(G)
    nodes = nx.betweenness_centrality(G)
    nids = []
    vals = []
    for k in nodes.keys():
        nids.append(k)
        vals.append(nodes[k])
    vals_adj = []
    
    m = max(vals)
    for v in vals:
        if v == 0:
            vals_adj.append(0)
        else:
            r = (v/m)
            vals_adj.append(r * 0.01)
    
    fig, ax = pt.generate_plot(G)

    ps = []
    for nid, buff_dist in zip(nids, vals_adj):
        n = G.node[nid]
        if buff_dist > 0:
            p = Point(n['x'], n['y']).buffer(buff_dist)
            ps.append(p)
        
    gpd.GeoSeries(ps).plot(ax=ax, color='r', alpha=0.75)
    
    
if __name__ == '__main__':
    main()
    