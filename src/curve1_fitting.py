'''curve1.dat fitting
'''
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import utils

# Read the original data from file
data = open("../data/curve1.dat","r").read().split("\n")
data.pop()
data = [float(x) for x in data]

# Remove the anomaly in data points, data[63]=500, so it doesn't affect optimization
#data63 = data[63]
#data[63] = (data[62]+data[64])/2

# Only optimize this type of model wrt data points 0...99
data=[data[x] for x in range(1000)]

# The general model class used for optimization
def fun(x, a, b, c, d, e, f):
    val = np.array([(a-b*xi)*(np.abs(np.cos(c*xi + d))-1)+e for xi in x])
    for i in range(len(x)):
        if val[i] > f:
            val[i] = f
    return val

# Function with a rough approximation of the optimized parameters
def funopt(x):
        val = np.array([(1698-10.79*xi)*(np.abs(np.cos(-0.11+(xi + 1)/6))-1)+484 for xi in x])
        for i in range(len(x)):
                if val[i] > 0:
                        val[i] = 0
        return np.round(val)

# Optimization using scipy.opitmize.curve_fit
ran = np.linspace(0,99,num=1000)
popt, popcov = curve_fit(fun, ran, data, p0 = [1700, 12, 1.0/6, 0, 500, 50])

# Plot data and fitted function
y=funopt(ran)
#y=fun(ran,*popt)
#data[63]=data63 # Just adding the anomaly in data back
plt.plot(data)
plt.plot(y);
plt.show()

# Counting and saving the differences between the fitted model and actual data
difference = data - y
rss = 0
for i in range(len(difference)):
    rss += difference[i]**2
print("Residual sum of squares: ",rss)
print min(difference), max(difference)
hf, enc, digs = utils.dig2enc(difference) 
print len(hf), len(hf) / 8
#np.savetxt("d",difference,"%d")    