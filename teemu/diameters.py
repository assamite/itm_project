__author__ = 'teemupitkanen1'
import math
data=open("../data/paleo.csv","r").read().split("\n")
data.pop()
del data[0]
print(len(data))

dmismax1=0
dmismax2=0
maxes=0

for i in range(len(data)):
    record = data[i].split(';')
    dm=-1
    maxdm1=-1
    maxdm2=-1
    if(record[2]!=''):
        record[2]=record[2].replace(",",".")
        maxdm1=float(record[2])
    if(record[3]!=''):
        record[3]=record[3].replace(",",".")
        dm=math.ceil(float(record[3]))
    if(record[9]!=''):
        record[9]=record[9].replace(",",".")
        maxdm2=float(record[9])
    if dm==maxdm1:
        dmismax1=dmismax1+1
    if dm==maxdm2:
        dmismax2=dmismax2+1
    if dm!=maxdm1 and dm != maxdm2:
        maxes=maxes+1
print(dmismax1)
print(dmismax2)
print(maxes)
