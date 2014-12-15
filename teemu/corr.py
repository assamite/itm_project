import floatfields as flo
from matplotlib import pyplot as plt
def draw():
	a=flo.asfloats(11)
	b=flo.asfloats(4)
	c=flo.asfloats(5)
	y=[]
	for i in range(len(a)):
		if c[i]!=0:
			y.append((b[i]/c[i])-a[i])
		else:
			y.append(0)
	x=range(len(a))
	fig = plt.figure()
	ax=fig.add_subplot(111)
	ax.set_ylabel("(field 4 / field 5) - field 11")
	ax.set_xlabel("record index")
	ax.plot(x,y,'k.',markersize=2.0)
	plt.show()
