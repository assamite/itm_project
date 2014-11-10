import numpy as np
r=open("r","r").read().split("\n")
r.pop()
r=[float(x) for x in r]
[a,b,c,d,e,f,g,h,i,j]=[-1.08, 1363.0, 1.0/60, 15.0, 1.09,-28.15,-24.33,0.27,-0.7,2.64]
for n in range(2000):
	if(n<1250):
		r[n] = r[n]+(np.abs(a*n + b)) *(-1)* (np.abs(np.cos(c*n))-1)**2+d                
	else:
		r[n] = r[n]+(e*(n-1250) + f) * ( np.abs( np.cos((2*c)*(n-1250) + g) + h ) +i ) + j
np.savetxt("decompressed",r,"%.2f")
