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
data_all=data
data=[data[x] for x in range(1000)]

# The general model class used for optimization
def fun(x, a, b, c, d, e, f):
        val = np.array([(a-b*xi)*(np.cos(c*xi*2+d)+np.abs(np.cos(c*xi + d))-2)**4+e for xi in x])
#        for i in range(len(x)):
#                if val[i] > 0:
#                        val[i] = 0
        return val

# Function with a rough approximation of the optimized parameters
#def funopt(x):
#        val = np.array([(1698-10.79*xi)*(np.abs(np.cos((xi + 1)/6))-1)+484 for xi in x])
#        for i in range(len(x)):
#                if val[i] > 34:
#                        val[i] = 34
#        return np.round(val)

# Optimization using scipy.opitmize.curve_fit
ran = np.linspace(0,999,num=1000)
popt, popcov = curve_fit(fun, ran, data, p0 = [1700, 12, 1.0/60, 0, 500, 50])
ran2 = np.linspace(0,1999,num=2000)
# Plot data and fitted function
#y=funopt(ran2)
y=fun(ran2,*popt)
#data[63]=data63 # Just adding the anomaly in data back

y2 = fun(ran, *popt)
res = y2 - data
plt.plot(data[:200])
plt.plot(res[:200]);
plt.plot(y2[:200])
plt.show()

#cut res to 2 decimal precision
resc = [float("{:.2f}".format(e)) for e in res]
hf, enc, digits = utils.dig2enc(resc)
enc, bts, add = utils.nums2bin(resc, filepath='test')
print enc, len(bts), add
nums = utils.bin2nums('test', enc, len(bts), add)
print nums == resc
print "Huffman code bits {}, bytes {}".format(len(hf), np.ceil(float(len(hf)) / 8))
