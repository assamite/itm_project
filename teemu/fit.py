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
	for n in range(len(x)):
		if(n<1250):
			val[n] = (abs(a*x[n] + b)) *(-1)* (np.abs(np.cos(c*x[n]))-1)**2+d
        	else:
			val[n] = (e*(x[n]-1250) + f) * ( np.abs( np.cos(g*(x[n]-1250) + h) + i ) +j ) + k	
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
quessed_params = [-1.08, 1363, 1.0/60, 15, 1.09,-28.15,1.0/30,-24.33,0.27,-0.7,2.64]
popt, popcov = curve_fit(fun, ran, data, p0 = quessed_params)

# Plot data, the fitted function and the difference
y=fun(ran,*popt)
plt.plot(data)
plt.plot(y);
#plt.plot(data-y)
plt.show()
np.savetxt("optimal_params_all",popt,"%f")

estimates = fun(ran, *quessed_params)
estimates = [round(x,2) for x in estimates]
residuals = np.array(data)-np.array(estimates)
np.savetxt("d",residuals,"%.2f")
