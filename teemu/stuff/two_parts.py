import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

# Read the original data from file
data = open("../data/curve1.dat","r").read().split("\n")
data.pop()
data = [float(x) for x in data]

# The general model class used for optimization
def fun(x, a, b, c, d, e, f, g, h, i, j, k):
        val = [0 for n in range(len(x))]
        for n in x:
                if(n<1250):
                        val[n] = (np.abs(a*x[n] + b)) *(-1)* (np.abs(np.cos(c*x[n]))-1)**2+d
                else:
                        val[n] = (e*(x[n]-1250) + f) * ( np.abs( np.cos(g*(x[n]-1250) + h) + i ) +j ) + k
        return np.array(val)

# Optimization using scipy.opitmize.curve_fit
ran = np.linspace(0,1999,num=2000)
quessed_params = [-1.08, 1363, 1.0/60, 15, 1.09,-28.15,1.0/30,-24.33,0.27,-0.7,2.64]
popt, popcov = curve_fit(fun, ran, data, p0 = quessed_params)

y=fun(ran,*popt)
smaller=[]
smalleri=[]
bigger=[]
biggeri=[]
for ii in range(2000):
	if y[ii]>data[ii]:
		bigger.append(data[ii])
		biggeri.append(ii)
	else:
		smaller.append(data[ii])
		smalleri.append(ii)
plt.plot(y)
plt.plot(biggeri,bigger)
plt.plot(smalleri,smaller)
plt.show()
