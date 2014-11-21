__author__ = 'teemupitkanen1'
import numpy as np

data=open("../data/paleo.csv","r").read().split("\n")
del data[0]
data.pop()

# Create array "accuracy". accuracy[i,j] = places after decimal points for data record i, field 10+j
accuracy = []
for i in range(len(data)):
    row=[0,0,0]
    record = data[i].split(";")
    for indx in range(0,3):
        if record[10+indx]=='':
            row[indx]=-1
        elif record[10+indx]=='#DIV/0!':
            row[indx]=-2
        else:
            temp = record[10+indx].split(",")
            if len(temp)==2:
                row[indx]=len(temp[1])

    # Set length of fields with arbitrary values to -3
    record[0]='0'
    for k in range(len(record)):
        if record[k]=='' or record[k]=='#DIV/0!':
            record[k]='0'
        else:
            record[k]=record[k].replace(",",".")
        record[k]=float(record[k])

    if record[3]==0:
        if record[10]!=0:
            row[0]=record[10]
        if record[12]!=0:
            row[2]=record[12]
    else:
        if record[10] != round(record[4]/record[3], row[0]):
            row[0]=record[10]
        if record[12] != round(record[6]/record[3], row[2]):
            row[2]=record[12]
    if record[5]==0:
        if record[11]!=0:
            row[1]=record[11]
    elif record[11] != round(record[4]/record[5], row[1]):
        row[1]=+record[11]
    row = [str(x) for x in row]
    accuracy.append(row)
    print(row)
np.savetxt("a",accuracy,'%s')