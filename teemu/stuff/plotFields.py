import floatfields
from matplotlib import pyplot as plt
def plotField(field):
	data = floatfields.asfloats(field)
	plt.plot(data)
	plt.show()
