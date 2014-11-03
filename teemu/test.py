import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

data = file("curve1.dat","r").read().split("\n")
data.pop()
data = [int(x) for x in data]
data63 = data[63]
data[63] = data[62]
data=[data[x] for x in range(100)]

def fun(x, a, b, c, d, e, f):
	val = np.array([(a-b*xi)*(np.abs(np.cos(c*xi + d))-1)+e for xi in x])
	for i in range(len(x)):
		if val[i] > f:
			val[i] = f
	return val

ran = np.linspace(0,99,num=100)

popt, popcov = curve_fit(fun, ran, data, p0 = [1700, 12, 1.0/6, 0, 500, 50])

y=fun(ran,*popt)

data[63]=data63
plt.plot(data)
plt.plot(y);

difference = data - np.round(fun(ran,*popt))
np.savetxt("diff.dat",difference,"%3d")	
plt.show()

