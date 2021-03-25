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
#Load annotation data
data_table=pd.read_table('GSE60361_series_matrix.txt',sep='\t',index_col=0)
annotations=np.array(data_table)
cell_type=annotations[6]

#Gene filtering
existenceCutoff=0.2
geneFilter=np.sum(log_data>1,1)/len(log_data[0])>existenceCutoff
log_data=log_data[geneFilter,:]
gene_name=gene_name[geneFilter]

#### make correlation network 4 gene
#Sort by CV
log_data_mean4gene=np.mean(log_data,axis=1)
log_data_std4gene=np.std(log_data,axis=1)
log_data_CV4gene=log_data_std4gene/log_data_mean4gene
sortIndex=np.argsort(log_data_CV4gene)
sortIndex=sortIndex[::-1]
highCutoff=100
#Calculation correlation matrix
log_data_corr4gene=np.corrcoef(log_data[sortIndex[0:highCutoff],:])
np.fill_diagonal(log_data_corr4gene,0)
corrCutoff=0.7
log_data_corr4gene[np.abs(log_data_corr4gene)<corrCutoff]=0
#Make a network
corrNetwork4gene=nx.to_networkx_graph(log_data_corr4gene,create_using=nx.Graph)
#Node labeling
node_labels={};
for i in range(highCutoff):
    node_labels[i]=gene_name[sortIndex[i]]
corrNetwork4gene=nx.relabel_nodes(corrNetwork4gene,node_labels)
lcc_node = max(nx.connected_components(corrNetwork4gene),key=len)
corrNetwork4geneLcc=corrNetwork4gene.subgraph(lcc_node)
nx.draw_networkx(corrNetwork4geneLcc)
nx.write_weighted_edgelist(corrNetwork4geneLcc,"corrNetwork4geneCVhigh"+str(highCutoff)+"pcc"+str(corrCutoff)+".txt",delimiter="\t")

#### make correlation network 4 cell
#Sort by CV
log_data_mean4cell=np.mean(log_data,axis=0)
log_data_std4cell=np.std(log_data,axis=0)
log_data_CV4cell=log_data_std4cell/log_data_mean4cell
sortIndex=np.argsort(log_data_CV4cell)
sortIndex=sortIndex[::-1]
highCutoff=100
#Calculation correlation matrix
log_data_corr4cell=np.corrcoef(np.transpose(log_data[:,sortIndex[0:highCutoff]]))
np.fill_diagonal(log_data_corr4cell,0)
corrCutoff=0.4
log_data_corr4cell[np.abs(log_data_corr4cell)<corrCutoff]=0
#Make a network
corrNetwork4cell=nx.to_networkx_graph(log_data_corr4cell,create_using=nx.Graph)
#Node labeling
node_labels={};
for i in range(highCutoff):
    node_labels[i]=cell_id[sortIndex[i]]
corrNetwork4cell=nx.relabel_nodes(corrNetwork4cell,node_labels)
lcc_node = max(nx.connected_components(corrNetwork4cell),key=len)
corrNetwork4cellLcc=corrNetwork4cell.subgraph(lcc_node)
nx.draw_networkx(corrNetwork4cellLcc)
nx.write_weighted_edgelist(corrNetwork4cellLcc,"corrNetwork4cellCVhigh"+str(highCutoff)+"pcc"+str(corrCutoff)+".txt",delimiter="\t")

#Write annotation file
ofile = open("cell_type.txt","w")
for i in range(len(cell_id)):
    ofile.write(cell_id[i]+"\t"+cell_type[i]+"\n")
ofile.close()