import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

# Read the original data from file
data = file("curve1.dat","r").read().split("\n")
data.pop()
data = [int(x) for x in data]

# Remove the anomaly in data points data[63] so it doesn't affect optimization
data63 = data[63]
data[63] = (data[62]+data[64])/2

# Only optimize this type of model wrt data points 0...99
data=[data[x] for x in range(100)]

# The model function
def fun(x, a, b, c, d, e, f):
	val = np.array([(a-b*xi)*(np.abs(np.cos(c*xi + d))-1)+e for xi in x])
	for i in range(len(x)):
		if val[i] > f:
			val[i] = f
	return val

# Optimization using scipy.opitmize.curve_fit
ran = np.linspace(0,99,num=100)
popt, popcov = curve_fit(fun, ran, data, p0 = [1700, 12, 1.0/6, 0, 500, 50])

# Plot data and fitted function
y=fun(ran,*popt)
data[63]=data63 # Just adding the anomaly in data back
plt.plot(data)
plt.plot(y);
plt.show()

# Counting and saving the differences between the fitted model and actual data
difference = data - np.round(fun(ran,*popt))
np.savetxt("diff.dat",difference,"%3d")	

