def extract(field):
	all_data = open("../data/paleo.csv","r").read().split("\n")
	all_data.pop()
	datafield=[]
	for x in all_data:
		temp = x.split(";")
		datafield.append(temp[field])
	datafield.pop()
	return datafield
