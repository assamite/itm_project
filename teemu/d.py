import numpy as np
r= open("r","r").read().split("\n")
r.pop()
r=[float(x) for x in r]
for n in range(2000):
	if(n<1250):
		r[n]=r[n]-(np.abs(-1.08*n+1363))*(np.abs(np.cos(n*1.0/60))-1)**2+15                
	else:
		r[n]=r[n]+(1.09*(n-1250)-28.15)*(np.abs(np.cos((1.0/30)*(n-1250)-24.33)+0.27)-0.7)+2.64
np.savetxt("curve1.dat",r,"%.2f")
