__author__ = 'teemupitkanen1'
import bz2, sys
data=open("../data/caravan.dat","r").read().split("\n")[:-1]
#side=open("../sdata/caravan.sdat","r").read().split("\n")[:-1]
#cbought=['']*85
#cdidnt=['']*85
#columns=['']*85
column0=[]
column4=[]
for i  in range(len(data)):
    record=data[i].split("\t")
    column0.append(record[0])
    column4.append(record[42])
    #for j in range(85):
        #columns[j]+=record[j]
        #if side[i]=='1':
        #    cbought[j]+=record[j]+','
        #else:
        #    cdidnt[j]+=record[j]+','

#bits = bz2.compress(cbought[0])+bz2.compress(cdidnt[0])
#bits = bz2.compress(columns[0])
#for i in range(1,85):
#    bits+=bz2.compress(columns[i])
    #bits+=bz2.compress(cbought[i])+bz2.compress(cdidnt[i])
#sys.stdout.write(bits)
errors=0;
pairs = {}
for i in range(len(data)):
    if pairs.has_key(column0[i]):
        if pairs.get(column0[i]) != column4[i]:
            errors+=1
            print(i)
            print(column0[i])
            print(pairs.get(column4[i]))
            print '-------'
    else:
        pairs[column0[i]]=column4[i]
print 'errors: '+str(errors)
print pairs