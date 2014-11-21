__author__ = 'teemupitkanen1'
data=open("a","r").read().split("\n")
data.pop()
list = range(10)
list = [str(x) for x in list]
for i in range(len(data)):
    record = data[i]
    for j in range(3):
        temp = record[j]
        temp=temp[1:]
        if temp in list:
            print('noooooo')