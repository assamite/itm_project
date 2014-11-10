import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

data = open("../data/curve1.dat","r").read().split("\n")
data.pop()
data = [float(data[x]) for x in range(1250,2000)]
def fun(x,a,b,c,d,e,f,g):
	val =	np.array([(a*xi + b) * ( np.abs( np.cos(c*xi + d) + e ) -1+e +f ) + g for xi in x]) 
	return val
ran = np.linspace(0,749,num=750)
quessed_params = [0.5,10,0.035,-25,0.5,0,0]
params, covar = curve_fit(fun, ran, data, p0 = quessed_params)

y = fun(ran,*params)
plt.plot(y)
plt.plot(data)
plt.show()

residuals = data-y
#plt.plot(residuals)
#plt.show()
print(residuals)

