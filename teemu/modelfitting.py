import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

# Read the original data from file
data = open("../data/curve1.dat","r").read().split("\n")
data.pop()
data = [float(x) for x in data]

# At this point, I optimize only wrt the first 1000 datapoints
data_all=data
data=[data[x] for x in range(1000)]

# The general model class used for optimization
def fun(x, a, b, c, d):
# 	val = np.array[-np.abs((a+bxi)*(np.cos(c*xi+d))-1)**2]     
	val = np.array([ (abs(b*((-xi)/a + 1))) *(-1)* (np.abs(np.cos(c*xi))-1)**2+d for xi in x])
        return val

# Optimization using scipy.opitmize.curve_fit
ran = np.linspace(0,999,num=1000)
popt, popcov = curve_fit(fun, ran, data, p0 = [1200, 1300, 1.0/60, 500])
ran2 = np.linspace(0,1999,num=2000)

# Plot data, the fitted function and the difference
y=fun(ran2,*popt)
plt.plot(data_all)
plt.plot(y);
plt.plot(data_all-y)
plt.show()
np.savetxt("optimal_params",popt,"%f")
