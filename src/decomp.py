import sys,struct
import numpy as np
f=open(sys.argv[1]).read()
b=reduce(lambda x,y:x+'{:08b}'.format(y),struct.unpack('4000B',f),"")
p=[-1.08,1363,1.0/60,15,1.09,-28.15,1.0/30,-24.33,0.27,-0.7,2.64]
def m(n,a,b,c,d,e,f,g,h,i,j,k):
    if(n<1250):
        return (-1*np.abs(a*n+b))*(np.abs(np.cos(c*n))-1)**2+d
    else:
        return (e*(n-1250)+f)*(np.abs(np.cos(g*(n-1250)+h)+i)+j)+k    
r=range(149)+[150,151,153,154,155,158,159,161,162,164,165,167,169,170,171,172,173,174,177,178,182,183,195,196,197,200,204,209,228,233,243,245,256,276,342]
a=2000
i=[float(x+y+"."+z) for x,y,z in zip(["-" if x=='0' else '' for x in b[:a]],map(lambda x:str(r[int("".join(x),2)]),zip(*[iter(b[a:a*9])]*8)),map(lambda x:"{:02d}".format(int("".join(x),2)),zip(*[iter(b[a*9:])]*7)))]
sys.stdout.write("\n".join(["{:.2f}".format(round(m(i,*p),2)+a) for i,a in enumerate(i)])+"\n")
