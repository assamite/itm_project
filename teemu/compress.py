import numpy as np

data = open("../data/paleo.csv","r").read().split("\n")
data.pop()
del data[0] #header line, has to be added!!
comprsd=[]

for i in range(len(data)):
	record=data[i]
	fields = record.split(";")
	for j in range(10,13):
		field = fields[j].split(",")
		if len(field)==0:
			fields[j]='?'
		elif len(field)==2:
			fields[j]=len(field[1])
		else:
			if field=='#DIV/0!':
				fields[j]='#'
			else:
				fields[j]=0
	comprsd.append(fields)
print(comprsd)
