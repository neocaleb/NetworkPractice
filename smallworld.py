#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 10:03:10 2022

@author: qkx875
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

#Generate Regular graph
nodeSize=100
halfDegree=2
regularNetwork=nx.empty_graph()
for i in range(nodeSize):
    for j in range(halfDegree):
        if i+j+1<nodeSize:
            regularNetwork.add_edge(i,i+j+1)
        else:
            regularNetwork.add_edge(i,i+j+1-nodeSize)
nx.draw_networkx(regularNetwork)
nx.average_clustering(regularNetwork)
nx.average_shortest_path_length(regularNetwork)


randomNum=100
nSwapRange=np.arange(1,21,1)
CC=np.zeros((len(nSwapRange),randomNum))
CPL=np.zeros((len(nSwapRange),randomNum))
for i in range(len(nSwapRange)):
    nSwap=nSwapRange[i]
    for j in range(randomNum):
        smallworldNetwork=regularNetwork.copy()
        nx.double_edge_swap(smallworldNetwork,nSwap,100)
        CC[i,j]=nx.average_clustering(smallworldNetwork)
        CPL[i,j]=nx.average_shortest_path_length(smallworldNetwork)

plt.plot(nSwapRange/nodeSize,np.mean(CPL,1)/max(np.mean(CPL,1)))
plt.plot(nSwapRange/nodeSize,np.mean(CC,1)/max(np.mean(CC,1)))
#plt.xscale('log')
plt.show()