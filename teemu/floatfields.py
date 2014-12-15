import extractFields
def asfloats(field):
        data = extractFields.extract(field)
        del data[0]
        data = [x.replace(",",".") for x in data]
        for i in range(len(data)):
                if data[i]=='':
                        data[i]='0'
                if data[i]=='#DIV/0!':
                        data[i]='0'
        data = [float(x) for x in data]
	return data


