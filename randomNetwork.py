#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 21:24:10 2021

@author: qkx875
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

#Generate Random Network
nodeSize=100
randomProb=0.1
randomArray=np.tril(np.random.random_sample([nodeSize,nodeSize]))
np.fill_diagonal(randomArray,0)
randomNetwork=nx.to_networkx_graph(randomArray>1-randomProb)
nx.draw_networkx(randomNetwork)

#Degree distribution
degree_sequence = [d for n, d in randomNetwork.degree()]
plt.hist(degree_sequence,bins='auto',density=1)
#Calculate number of edges (L) for random networks
randomNum=1000
Nedges=np.zeros(randomNum)
ClusteringCoeff=np.zeros(randomNum)
for i in range(randomNum):
    randomArray=np.tril(np.random.random_sample([nodeSize,nodeSize]))
    np.fill_diagonal(randomArray,0)
    randomNetwork=nx.to_networkx_graph(randomArray>1-randomProb)
    Nedges[i]=randomNetwork.number_of_edges()
    ClusteringCoeff[i]=nx.average_clustering(randomNetwork)
plt.hist(Nedges,bins='auto',density=1)
plt.hist(ClusteringCoeff,bins='auto',density=1)

#Evolution of random networks
nodeSize=100
randomProbRange=np.arange(0.001,0.031,0.001)
randomProbLccSize=np.zeros(len(randomProbRange))
for i in range(len(randomProbRange)):
    randomProb=randomProbRange[i]
    randomArray=np.tril(np.random.random_sample([nodeSize,nodeSize]))
    np.fill_diagonal(randomArray,0)
    randomNetwork=nx.to_networkx_graph(randomArray>1-randomProb)
    lcc_node = max(nx.connected_components(randomNetwork),key=len)
    randomNetworkLcc=randomNetwork.subgraph(lcc_node)
    randomProbLccSize[i]=randomNetworkLcc.number_of_nodes()
    
    #nx.draw_networkx(randomNetworkLcc)

plt.plot(randomProbRange,randomProbLccSize) #Network size by probability
plt.plot(randomProbRange*(nodeSize-1),randomProbLccSize) #Network size by average degree

randomNum=100
nodeSize=100
randomProbRange=np.arange(0.001,0.031,0.001)
randomProbLccSize=np.zeros([randomNum,len(randomProbRange)])
for i in range(randomNum):
    for j in range(len(randomProbRange)):
        randomProb=randomProbRange[j]
        randomArray=np.tril(np.random.random_sample([nodeSize,nodeSize]))
        np.fill_diagonal(randomArray,0)
        randomNetwork=nx.to_networkx_graph(randomArray>1-randomProb)
        lcc_node = max(nx.connected_components(randomNetwork),key=len)
        randomNetworkLcc=randomNetwork.subgraph(lcc_node)
        randomProbLccSize[i,j]=randomNetworkLcc.number_of_nodes()

for i in range(randomNum):
    plt.plot(randomProbRange*(nodeSize-1),randomProbLccSize[i,:]) #Network size by average degree
plt.imshow(randomProbLccSize)

#Average path length
averageDegree=3
nodeSizeRange=np.arange(100,1100,100)
CPL=np.zeros(len(nodeSizeRange))
for i in range(len(nodeSizeRange)):
    nodeSize=nodeSizeRange[i]
    randomProb=averageDegree/(nodeSize-1)
    randomArray=np.tril(np.random.random_sample([nodeSize,nodeSize]))
    np.fill_diagonal(randomArray,0)
    randomNetwork=nx.to_networkx_graph(randomArray>1-randomProb)
    lcc_node = max(nx.connected_components(randomNetwork),key=len)
    randomNetworkLcc=randomNetwork.subgraph(lcc_node)
    CPL[i]=nx.average_shortest_path_length(randomNetworkLcc)
plt.plot(nodeSizeRange,CPL)