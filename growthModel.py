#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 22:02:27 2021

@author: qkx875
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

#Growth model
nodeSize=20
startNodeNumber=2
addEdgeNumber=2
growthNetwork=nx.complete_graph(startNodeNumber)
for i in range(nodeSize-startNodeNumber):
    currentNodes=list(growthNetwork.nodes)
    selectedNodes=np.random.choice(len(currentNodes),addEdgeNumber,replace=False)
    for nodes in selectedNodes:
        growthNetwork.add_edge(nodes,i+startNodeNumber)
    nx.draw_networkx(growthNetwork)
    plt.show()
#Degree distribution
degree_sequence = [d for n, d in growthNetwork.degree()]
histFreq=np.histogram(degree_sequence,bins=100)
histFreqY=histFreq[0]/sum(histFreq[0])
histFreqX=histFreq[1][1:]
histFreqX=histFreqX[histFreqY>0]
histFreqY=histFreqY[histFreqY>0]
plt.scatter(histFreqX,histFreqY)
plt.xscale('log')
plt.yscale('log')

#Growth model with degree distribution
nodeSize=10000
startNodeNumber=2
addEdgeNumber=2
growthNetwork=nx.complete_graph(startNodeNumber)
for i in range(nodeSize-startNodeNumber):
    currentNodes=list(growthNetwork.nodes)
    selectedNodes=np.random.choice(len(currentNodes),addEdgeNumber,replace=False)
    for nodes in selectedNodes:
        growthNetwork.add_edge(nodes,i+startNodeNumber)
    if i%1000==997:
        #Degree distribution
        degree_sequence = [d for n, d in growthNetwork.degree()]
        histFreq=np.histogram(degree_sequence,bins=100)
        histFreqY=histFreq[0]/sum(histFreq[0])
        histFreqX=histFreq[1][1:]
        histFreqX=histFreqX[histFreqY>0]
        histFreqY=histFreqY[histFreqY>0]
        plt.scatter(histFreqX,histFreqY)
        plt.xscale('log')
        plt.yscale('log')

#Growth model with different m (addEdgeNumber)
nodeSize=1000
startNodeNumber=3
for addEdgeNumber in range(3):
    addEdgeNumber=addEdgeNumber+1
    growthNetwork=nx.complete_graph(startNodeNumber)
    for i in range(nodeSize-startNodeNumber):
        currentNodes=list(growthNetwork.nodes)
        selectedNodes=np.random.choice(len(currentNodes),addEdgeNumber,replace=False)
        for nodes in selectedNodes:
            growthNetwork.add_edge(nodes,i+startNodeNumber)
    #Degree distribution
    degree_sequence = [d for n, d in growthNetwork.degree()]
    histFreq=np.histogram(degree_sequence,bins=100)
    histFreqY=histFreq[0]/sum(histFreq[0])
    histFreqX=histFreq[1][1:]
    histFreqX=histFreqX[histFreqY>0]
    histFreqY=histFreqY[histFreqY>0]
    plt.scatter(histFreqX,histFreqY)
    plt.xscale('log')
    plt.yscale('log')
    
#Growth and preferential attachment
nodeSize=20
startNodeNumber=2
addEdgeNumber=2
BAnetwork=nx.complete_graph(startNodeNumber)
for i in range(nodeSize-startNodeNumber):
    currentNodes=list(BAnetwork.nodes)
    degree_sequence = [d for n, d in BAnetwork.degree()]
    selectedNodes=np.random.choice(len(currentNodes),addEdgeNumber,replace=False,p=np.array(degree_sequence)/sum(degree_sequence))
    for nodes in selectedNodes:
        BAnetwork.add_edge(nodes,i+startNodeNumber)        
    nx.draw_networkx(BAnetwork)
    plt.show()
#Degree distribution
degree_sequence = [d for n, d in BAnetwork.degree()]
histFreq=np.histogram(degree_sequence,bins=100)
histFreqY=histFreq[0]/sum(histFreq[0])
histFreqX=histFreq[1][1:]
histFreqX=histFreqX[histFreqY>0]
histFreqY=histFreqY[histFreqY>0]
plt.scatter(histFreqX,histFreqY)
plt.xscale('log')
plt.yscale('log')

#Growth and preferential attachment with degree distribution
nodeSize=10000
startNodeNumber=2
addEdgeNumber=2
BAnetwork=nx.complete_graph(startNodeNumber)
for i in range(nodeSize-startNodeNumber):
    currentNodes=list(BAnetwork.nodes)
    degree_sequence = [d for n, d in BAnetwork.degree()]
    selectedNodes=np.random.choice(len(currentNodes),addEdgeNumber,replace=False,p=np.array(degree_sequence)/sum(degree_sequence))
    for nodes in selectedNodes:
        BAnetwork.add_edge(nodes,i+startNodeNumber)        
    if i%1000==997:
        degree_sequence = [d for n, d in BAnetwork.degree()]
        histFreq=np.histogram(degree_sequence,bins=100)
        histFreqY=histFreq[0]/sum(histFreq[0])
        histFreqX=histFreq[1][1:]
        histFreqX=histFreqX[histFreqY>0]
        histFreqY=histFreqY[histFreqY>0]
        plt.scatter(histFreqX,histFreqY)
        plt.xscale('log')
        plt.yscale('log')

#Growth and preferential attachment with different m (addEdgeNumber)
nodeSize=1000
startNodeNumber=3
for addEdgeNumber in range(3):
    addEdgeNumber=addEdgeNumber+1
    BAnetwork=nx.complete_graph(startNodeNumber)
    for i in range(nodeSize-startNodeNumber):
        currentNodes=list(BAnetwork.nodes)
        degree_sequence = [d for n, d in BAnetwork.degree()]
        selectedNodes=np.random.choice(len(currentNodes),addEdgeNumber,replace=False,p=np.array(degree_sequence)/sum(degree_sequence))
        for nodes in selectedNodes:
            BAnetwork.add_edge(nodes,i+startNodeNumber)        
    
    degree_sequence = [d for n, d in BAnetwork.degree()]
    histFreq=np.histogram(degree_sequence,bins=100)
    histFreqY=histFreq[0]/sum(histFreq[0])
    histFreqX=histFreq[1][1:]
    histFreqX=histFreqX[histFreqY>0]
    histFreqY=histFreqY[histFreqY>0]
    plt.scatter(histFreqX,histFreqY)
    plt.xscale('log')
    plt.yscale('log')
