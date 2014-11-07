import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

# Read the original data from file
data = open("../data/curve1.dat","r").read().split("\n")
data.pop()
data = [float(x) for x in data]

# Only optimize this type of model wrt data points 0...99
data_all=data
data=[data[x] for x in range(1000)]

# The general model class used for optimization
def fun(x, a, b, c, d, e):
        val = np.array([ (abs(b*((-xi)/a + 1))) *(-1)* (np.abs(np.cos(c*xi + d))-1)**2+e for xi in x])
#	rang = np.linspace(1000,2000,num=1000)
#	for i in rang:
#		val = val+(f*(i-1000))*np.abs(np.sin(c*i +d))
        return val

# Optimization using scipy.opitmize.curve_fit
ran = np.linspace(0,999,num=1000)
#popt, popcov = curve_fit(fun, ran, data, p0 = [1700, 12, 1.0/60, 0, 500])
popt, popcov = curve_fit(fun, ran, data, p0 = [1200, 1300, 1.0/60, 0, 500])
ran2 = np.linspace(0,1999,num=2000)

# Plot data and fitted function
y=fun(ran2,*popt)
plt.plot(data_all)
plt.plot(y);
plt.show()
np.savetxt("optimal_params",popt,"%f")
