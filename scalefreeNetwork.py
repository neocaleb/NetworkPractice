#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 15:17:12 2021

@author: qkx875
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

#Generate Scale-free Network
nodeSize=100
degreeExp=2
minDegree=2
degreeTotal=np.array(range(minDegree-1,nodeSize-1),dtype='float32')+1
degreeProb=degreeTotal**(-degreeExp)
degreeProb=degreeProb/sum(degreeProb)
nodeDegree=np.zeros(nodeSize,dtype='int')
nodeDegreeProb=np.random.random_sample(nodeSize)
for i in range(nodeSize):
    for j in range(len(degreeProb)):
        if nodeDegreeProb[i]<sum(degreeProb[:j+1]):
            nodeDegree[i]=j+minDegree
            break

scalefreeNetwork=nx.empty_graph(nodeSize)
nodeDegreeTemp=np.array(nodeDegree)
while 1:
    selectList=np.where(nodeDegreeTemp>0)
    selectedLink=selectList[0][np.random.randint(len(selectList[0]),size=2)]
    scalefreeNetwork.add_edge(*tuple(selectedLink))
    nodeDegreeTemp[selectedLink]-=1
    if sum(nodeDegreeTemp)==0:
        break
#nx.draw_networkx(scalefreeNetwork)
lcc_node = max(nx.connected_components(scalefreeNetwork),key=len)
scalefreeNetworkLcc=scalefreeNetwork.subgraph(lcc_node)
nx.draw_networkx(scalefreeNetworkLcc)
#Degree distribution
degree_sequence = [d for n, d in scalefreeNetwork.degree()]
plt.hist(degree_sequence,bins='auto',density=1)

#Generate Random Network
edgeSize=scalefreeNetwork.number_of_edges()
randomProb=edgeSize*2/(nodeSize*(nodeSize-1))
randomArray=np.tril(np.random.random_sample([nodeSize,nodeSize]))
np.fill_diagonal(randomArray,0)
for i in range(nodeSize):
    randomNetwork=nx.to_networkx_graph(randomArray>1-randomProb)
#nx.draw_networkx(randomNetwork)
lcc_node = max(nx.connected_components(randomNetwork),key=len)
randomNetworkLcc=randomNetwork.subgraph(lcc_node)
nx.draw_networkx(randomNetworkLcc)
#Degree distribution
degree_sequence = [d for n, d in randomNetwork.degree()]
plt.hist(degree_sequence,bins='auto',density=1)