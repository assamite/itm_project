import floatfields as ff

dm=ff.asfloats(3)
ww=ff.asfloats(4)
wh=ff.asfloats(5)
uw=ff.asfloats(6)
wwdm=ff.asfloats(10)
wwwh=ff.asfloats(11)
uwdm=ff.asfloats(12)

data = open("../data/paleo.csv","r").read().split("\n")
data.pop()
del data[0]

fails=0
successes=0


for i in range(len(data)-1):
	record = data[i].split(";")
	temp = record[10]
	temp = temp.split(",")
	val=0
	if len(temp) == 2:
		val = len(temp[1])
	if dm[i] != 0:
		result = ww[i]/dm[i]
		result=round(result,val)
		if(result == wwdm[i]):
#			print('success')
#			print(result)
#			print(wwdm[i])
			successes=successes+1
		else:
			print('failure')
			print(i)
			print(val)
			print(result)
			print(wwdm[i])
			fails=fails+1
print(fails)
print(successes)
