import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import utils

# Read the original data from file
data = open("../data/curve1.dat","r").read().split("\n")
data.pop()
data = [float(x) for x in data]

# The general model class used for optimization
def fun(x, a, b, c, d, e, f, g, h, i, j, k,m):
	val = [0 for n in range(len(x))]
	for n in range(len(x)):
		if(n<1250*m):
			val[n] = (np.abs(a*x[n] + b)) *(-1)* (np.abs(np.cos(c*x[n]))-1)**2+d
		else:
			val[n] = (e*(x[n]-(1250*m)) + f) * ( np.abs( np.cos(g*(x[n]-(1250*m)) + h) + i ) +j ) + k	
	return np.array(val)

# Optimization using scipy.opitmize.curve_fit
#-1.081736
#1363.251968
#0.016690
#15.255884
#1.089823
#-28.151598
#0.033419
#-24.325895
#0.270522
#-0.698834
#2.638657
ran = np.linspace(0,1999,num=2000)
print ran[:10]
p = [-1.08, 1363, 1.0/60, 15, 1.09,-28.15,1.0/30,-24.33,0.27,-0.7,2.64, 1]
#p = [-1.08589, 1365.49, 0.016679, 58.559187,1.131426,5601.76666,0.033079,-25.24067,-0.302556,-0.706202,51.668242,5]
#popt, popcov = curve_fit(fun, ran, data, p0 = p)

# Plot data, the fitted function and the difference
y=fun(ran,*p)
plt.plot(data, '.', color = 'black', ms = 2, label = 'data points')
plt.plot(y, color = 'red', label = 'fitted curve');
#plt.plot(data-y)
#plt.ylim((-1200, 600))
plt.ylabel('value')
plt.xlabel('index')
plt.legend(loc = 0)
plt.show()
#np.savetxt("optimal_params_all",popt,"%f")

estimates = y
estimates = [round(x,2) for x in estimates]
residuals = np.array(data)-np.array(estimates)
plt.plot(residuals, '.', color = 'black', ms = 2, label = 'residuals')
#plt.plot(y, color = 'red', label = 'fitted curve');
#plt.plot(data-y)
plt.ylim((-300, 250))
plt.ylabel('value')
plt.xlabel('index')
plt.legend(loc = 0)
plt.show()
#np.savetxt


#enc,bts,add=utils.nums2bin(residuals)
#print len(bts), add, enc
#np.savetxt("curve1_res",residuals,"%.2f")
