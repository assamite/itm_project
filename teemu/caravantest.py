__author__ = 'teemupitkanen1'
import bz2, sys
data=open("../data/caravan.dat","r").read().split("\n")[:-1]
#side=open("../sdata/caravan.sdat","r").read().split("\n")[:-1]
#cbought=['']*85
#cdidnt=['']*85
columns=['']*85
for i  in range(len(data)):
    record=data[i].split("\t")

    for j in range(85):
        columns[j]+=record[j]
        #if side[i]=='1':
        #    cbought[j]+=record[j]+','
        #else:
        #    cdidnt[j]+=record[j]+','

#bits = bz2.compress(cbought[0])+bz2.compress(cdidnt[0])
bits = bz2.compress(columns[0])
for i in range(1,85):
    bits+=bz2.compress(columns[i])
    #bits+=bz2.compress(cbought[i])+bz2.compress(cdidnt[i])
sys.stdout.write(bits)

