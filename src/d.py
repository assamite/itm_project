import numpy as np
r=open("r","r").read().split("\n")
r.pop()
r=[float(x) for x in r]
a,b,c,d,e,f,g,h,i,j=-1.08,1363.0,1.0/60,15.0,1.09,-28.15,-24.33,0.27,-0.7,2.64
x=[r[n]+(-1*np.abs(a*x+b))*(np.abs(np.cos(c*x))-1)**2+d if(n<1250)else r[n]+(e*(x-1250)+f)*(np.abs(np.cos((2*c)*(x-1250)+g)+h)+i)+j for n,x in enumerate(r)]
np.savetxt("decompressed",x,"%.2f")
