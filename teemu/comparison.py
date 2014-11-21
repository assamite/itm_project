__author__ = 'teemupitkanen1'
import numpy as np
data = open("../data/paleo.csv","r").read().split("\n")
data.pop()
cols=[]
for i in range(len(data)):
    row=data[i].split(";")
    line=row[10]+';'+row[11]+';'+row[12]+';'
    cols.append(line)
np.savetxt("comp",cols,'%s')