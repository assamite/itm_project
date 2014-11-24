'''Ty.txt Huffman coding decompression test.
'''
import sys,struct,numpy as np

def m(n,y,a,b,c,d,e,f,g,h,i,j,k,x):
    if(y<1250*x):
        return (-1*np.abs(a*n+b))*(np.abs(np.cos(c*n))-1)**2+d
    else:
        return (e*(n-1250*x)+f)*(np.abs(np.cos(g*(n-1250*x)+h)+i)+j)+k

f = open(sys.argv[1]).read()
b=reduce(lambda x,y:x+'{:08b}'.format(y),struct.unpack('{}B'.format(len(f)),f),"")
l=int(b[:8],2)
b=b[8:]
c = []
v = []
e = []
p=[-1.08589,1365.49,0.016679,64.559187,1.131426,5601.76666,0.033079,-25.24067,-0.302556,-0.706202,57.668242,5.0]
r=range(256)
r[210:216]=[347,5578,6625,7898,8650,9622]
o=10000
s=b[:o]
b=b[o:]
h=int(b[:8],2)
b=b[8:]
for i in xrange(h):
    c.append(int(b[:8],2))
    b=b[8:]
    v.append(int(b[:8],2))
    b=b[8:]
for i in xrange(h):
    e.append(b[:v[i]])
    b = b[v[i]:]
b = b[:-2]
u=[]
while len(b)>0:
    i=np.where(map(lambda x:b.startswith(x),e))[0][0]
    u.append(r[c[i]])
    b=b[len(e[i]):]
i=u[:o]
d=["{:02d}".format(e) for e in u[o:]]
ret = [float(x+y+"."+z) for x,y,z in zip(["-"if x=='0'else''for x in s],[str(x) for x in i],d)]
n=np.linspace(0,1999,o)
re2 =  ["{:.2f}".format(round(m(n[x],x,*p),2)+a) for x,a in enumerate(ret)] 
sys.stdout.write("\n".join([i[:-3] if i[-2:]=='00'else (i[:-1] if i[-1]=='0'else i) for i in re2])+"\n")
    
