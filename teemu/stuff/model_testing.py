import numpy as np
from matplotlib import pyplot as plt

params = open("optimal_params","r").read().split("\n")
params.pop()
params = [float(x) for x in params]
a = params[0]
b = params[1]
c = params[2]
d = params[3]
e = params[4]

def fun(x, a, b, c, d, e):
	val = np.array([ (abs(b*((-xi)/a + 1))) *(-1)* (np.abs(np.cos(c*xi + d))-1)**2+e for xi in x])
       	rang = np.linspace(1000,1999,num=1000)
	for i in rang:
		val[i] = val[i]+(0.2*(i-1000))*np.abs(np.cos(c*i + 2*c + d))
	return val

x = np.linspace(0,1999,num=2000)
plt.plot(fun(x,a,b,c,d,e))
plt.show()
