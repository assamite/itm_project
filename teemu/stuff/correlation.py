import floatfields as flo
from matplotlib import pyplot as plt
def draw(field1, field2):
	x= flo.asfloats(field1)
	y= flo.asfloats(field2)
	plt.plot(x,y,'ro')
	plt.show()
