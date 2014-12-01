__author__ = 'teemupitkanen1'
import numpy as np, math,sys,bz2

data=open("../data/paleo.csv","r").read().split("\n")
#print(data)
firstline=data[0]
del data[0]
data.pop()

data=[x.replace(",",".") for x in data]

# Create array "accuracy". accuracy[i,j] = places after decimal points for data record i, field 10+j
accuracy = []
for i in range(len(data)):
    row=[0,0,0,0]
    record = data[i].split(";")
    for indx in range(0,4):
        if record[10+indx]=='':
            row[indx]='a'
        elif record[10+indx]=='#DIV/0!':
            row[indx]='b'
        else:
            temp = record[10+indx].split(".")
            if len(temp)==2:
                row[indx]=len(temp[1])

    # Set special values for exceptions
    for k in range(1,len(record)):
        if record[k]=='' or record[k]=='#DIV/0!':
            record[k]='0'
        record[k]=float(record[k])

    if record[3]==0:
        if record[10]!=0 and row[0] not in ['a','b']:
            row[0]=record[10]
        if record[12]!=0 and row[2] not in ['a','b']:
            row[2]=record[12]
    else:
        if row[0] not in ['a','b'] and record[10] != round(record[4]/record[3], row[0]):
            row[0]=record[10]
        if row[2] not in ['a','b'] and record[12] != round(record[6]/record[3], row[2]):
            row[2]=record[12]
    if record[5]==0:
        if record[11]!=0 and row[1] not in ['a','b']:
            row[1]=record[11]
    elif row[1] not in ['a','b'] and record[11] != round(record[4]/record[5], row[1]):
  #      row[1]=+record[11] WHATWHATWHAT ilmeisesti typo, vaikka on toiminut
        row[1]=record[11]

    # WER!
    if(record[3]-record[7]==0) and row[3] not in ['a','b']:
        row[3]=record[13]
    elif row[3] not in ['a','b'] and record[13] != round((record[3]/(record[3]-record[7]))**2,row[3]):
        row[3]=record[13]

    row = [str(x) for x in row]
    accuracy.append(row)
np.savetxt("a",accuracy,'%s')

maxdm1 = []
maxdm2 = []
for i in range(len(data)):
    record=data[i].split(";")
    try:dm = str(int(math.ceil((float(record[3])))))
    except: dm=''
    if record[2] == dm:
        maxdm1.append('a')
    else:
        maxdm1.append(str(record[2]))
    if record[9] == dm:
        maxdm2.append('a')
    elif record[9]==record[2]:
        maxdm2.append('b')
    else:
        maxdm2.append(str(record[9]))

lobes=[]
for i in reversed(range(len(data))[1:]):
    record=data[i].split(";")
    record2=data[i-1].split(";")
    if record[8]==record2[8]:
        lobes.append('a')
    else:
        lobes.append(record[8])
lobes.append(data[0].split(";")[8])


newdata=[]
newdata.append(firstline)
newstring=firstline
for i in range(len(data)):
    newrecord=''
    record = data[i].split(";")
    for j in range(len(record)):
        if j!= 2 and j!=8 and j!=9 and j!=10 and j!=11 and j!=12 and j!=13:
            newrecord += (record[j]+';')
        elif j==2:
            newrecord += (str(maxdm1[i])+';')
        elif j==8:
            newrecord += lobes[len(data)-i-1]+';'
        elif j==9:
            newrecord += (str(maxdm2[i])+';')
        elif j==10:
            newrecord += (str(accuracy[i][0])+';')
        elif j==11:
            newrecord += (str(accuracy[i][1])+';')
        elif j==12:
            newrecord += (str(accuracy[i][2])+';')
        else:
            newrecord += (str(accuracy[i][3])+';')
    newdata.append(newrecord)
    newstring+=newrecord+'\n'
strings=['','','','','','','','','','','','','','']
del newdata[0]
for i in range(len(data)):
    record=newdata[i].split(";")
    for j in range(14):
        strings[j]+=record[j]+';'
bits=bz2.compress(firstline)
for i in range(0,14):
    bits+=bz2.compress(strings[i])

sys.stdout.write(bits)

