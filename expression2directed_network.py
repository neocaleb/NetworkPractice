# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


#Load expression data
data_table=pd.read_table('GSE60361_C1-3005-Expression_compressed.txt',sep='\t',index_col=0)
data_matrix=np.array(data_table)
cell_id=np.array(data_table.columns)
gene_name=np.array(data_table.index)
log_data=np.log2(data_matrix+1)

#Gene filtering & Cell filtering
existenceCutoff=0.2
geneFilter=np.sum(log_data>1,1)/len(log_data[0])>existenceCutoff
cellFilter=np.sum(log_data>1,0)/len(log_data)>existenceCutoff
log_data=log_data[geneFilter,:]
log_data=log_data[:,cellFilter]
gene_name=gene_name[geneFilter]

#### cell ordering
#Calculation correlation matrix for cells
log_data_corr4cell=np.corrcoef(np.transpose(log_data))
farthestCell=np.unravel_index(np.argmin(log_data_corr4cell,axis=None),log_data_corr4cell.shape)
cellSortIndex1=np.argsort(log_data_corr4cell[farthestCell[0],:])[::-1]
cellSortIndex2=np.argsort(log_data_corr4cell[farthestCell[1],:])[::-1]

#### make lagged correlation network for gene
#Calculation correlation matrix for gene
laggingRange=20
lagCorr4geneTotal=np.zeros((len(log_data),len(log_data),laggingRange))
for i in range(laggingRange):
    temp=np.corrcoef(log_data[:,cellSortIndex1[i+1:]],log_data[:,cellSortIndex1[:-i-1]])
    temp=temp[len(log_data):,:len(log_data)]
    lagCorr4geneTotal[:,:,i]=abs(temp)

lagCorr4gene=np.max(lagCorr4geneTotal,axis=2)
#Make a network
corrCutoff=0.7
lagCorrNetwork4gene=nx.from_numpy_matrix(lagCorr4gene>corrCutoff,create_using=nx.DiGraph)
#Node labeling
node_labels={};
for i in range(len(gene_name)):
    node_labels[i]=gene_name[i]
lagCorrNetwork4gene=nx.relabel_nodes(lagCorrNetwork4gene,node_labels)
#connected components
lcc_node = max(nx.weakly_connected_components(lagCorrNetwork4gene),key=len)
lagCorrNetwork4geneLcc=lagCorrNetwork4gene.subgraph(lcc_node)
nx.draw_networkx(lagCorrNetwork4geneLcc)
nx.write_weighted_edgelist(lagCorrNetwork4geneLcc,"lagCorrNetwork4gene_pcc"+str(corrCutoff)+".txt",delimiter="\t")

