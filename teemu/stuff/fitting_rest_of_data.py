import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

data_all = open("../data/curve1.dat","r").read().split("\n")
data_all.pop()
data = [float(data_all[x]) for x in range(1250,2000)]
data_all = [float(x) for x in data_all]

def fun(x,a,b,c,d,e,f,g):
	val =	np.array([(a*xi + b) * ( np.abs( np.cos(c*xi + d) + e ) +f ) + g for xi in x]) 
	return val

ran = np.linspace(0,749,num=750)
quessed_params = [0.5,10,0.035,-25,0.5,-1,0]
params, covar = curve_fit(fun, ran, data, p0 = quessed_params)

ran2=np.linspace(0,1999,num=2000)
y = fun(ran2-1250,*params)
plt.plot(y)
plt.plot(data_all)
plt.show()

residuals = data_all-y
#plt.plot(residuals)
#plt.show()
print(residuals)
np.savetxt("optimal_params2",params,"%f")
