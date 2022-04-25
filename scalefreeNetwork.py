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
sortIndex=np.argsort(nodeDegree)
sortIndex=sortIndex[::-1]
nodeDegreeTemp=np.array(nodeDegree)
for i in range(nodeSize):
    selectedNode=sortIndex[i]
    if nodeDegreeTemp[selectedNode]:
        selectList=list(np.where(nodeDegreeTemp>0)[0])
        selectList.remove([selectedNode])
        selectList=np.array(selectList)
        if nodeDegreeTemp[selectedNode]>len(selectList):
            selectedLink=selectList[np.random.choice(len(selectList),len(selectList),replace=False)]
        else:
            selectedLink=selectList[np.random.choice(len(selectList),nodeDegreeTemp[selectedNode],replace=False)]
        for j in range(len(selectedLink)):
            scalefreeNetwork.add_edge(*(selectedNode,selectedLink[j]))
        nodeDegreeTemp[selectedLink]-=1
        nodeDegreeTemp[selectedNode]=0
        if sum(nodeDegreeTemp>0)<=1:
            break
#nx.draw_networkx(scalefreeNetwork)
lcc_node = max(nx.connected_components(scalefreeNetwork),key=len)
scalefreeNetworkLcc=scalefreeNetwork.subgraph(lcc_node)
nx.draw_networkx(scalefreeNetworkLcc)
#Degree distribution
degree_sequence = [d for n, d in scalefreeNetwork.degree()]
plt.hist(degree_sequence,bins='auto')
plt.xscale("log")

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