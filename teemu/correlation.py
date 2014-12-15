import floatfields as flo
from matplotlib import pyplot as plt
def draw(field1, field2, name1, name2):
	x= flo.asfloats(field1)
	#y= flo.asfloats(field2)
	a=flo.asfloats(4)
	b=flo.asfloats(5)
	y=[]
	for i in range(len(a)):
		if b[i]!=0 and x[i]!=0:
			y.append((a[i]/b[i])/x[i])
		else:
			y.append(0)
	x=range(len(x))
	fig = plt.figure()
	ax=fig.add_subplot(111)
	ax.set_xlabel(name1)
	ax.set_ylabel(name2)
	ax.plot(x,y,’k.’)
	plt.show()