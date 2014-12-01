import sys,struct,re,numpy as np, math,bz2
f=open(sys.argv[1]).read()
b=reduce(lambda x,y:x+'{:08b}'.format(y),struct.unpack('{}B'.format(len(f)),f),"")
l=int(b[:8],2)
b=b[8:]
t=lambda x:np.linspace(0,1999,x)
def m(n,y,a,b,c,d,e,f,g,h,i,j,k,x):
    if(y<1250*x):
        return (-1*np.abs(a*n+b))*(np.abs(np.cos(c*n))-1)**2+d
    else:
        return (e*(n-1250*x)+f)*(np.abs(np.cos(g*(n-1250*x)+h)+i)+j)+k
def c(r,a,p):
    i=[float(x+y+"."+z) for x,y,z in zip(["-"if x=='0'else''for x in b[:a]],map(lambda x:str(r[int("".join(x),2)]),zip(*[iter(b[a:a*9])]*8)),map(lambda x:"{:02d}".format(int("".join(x),2)),zip(*[iter(b[a*9:])]*7)))]
    n=t(a)
    return ["{:.2f}".format(round(m(n[x],x,*p),2)+a) for x,a in enumerate(i)]  
if l==1:
    p=[-1.08,1363,1.0/60,15,1.09,-28.15,1.0/30,-24.33,0.27,-0.7,2.64,1.0]
    r=range(256)
    r[210:213]=[256,276,342]
    sys.stdout.write("\n".join([i for i in c(r,2000,p)])+"\n")
if l==2:
    w=[]
    k = [83,23899,6800,2214,5143,4558,4604,4270,1365,964,1381,1912,2607,1939,2153]
    o=1
    for x in range(15):
        w.append(bz2.decompress(f[o:o+k[x]]).split(";")[:-1])
        o=o+k[x]
    d=';'.join(w[0])+';WER\n'
    del w[0]
    j=''
    for x in range(4128):
        for l in range(14):
            if l in [0,1,3,4,5,6,7]:
                d+=(w[l][x])
            elif l in [2,9]:
                if w[l][x]=='a':
                    try:d+=(str(int(math.ceil(float(w[3][x])))))
                    except:pass
                elif w[l][x]=='b':d+=w[2][x]
                else: d+= w[l][x]
            elif l==8:
                if w[l][x]=='a':d+=j
                else:
                    j=w[l][x]
                    d+=j
            else:
                if w[l][x]=='b':d+='#DIV/0!'
                elif w[l][x]!='a':
                    try:
                        if l==10:v=float(w[4][x])/float(w[3][x])
                        elif l==11:v=float(w[4][x])/float(w[5][x])
                        elif l==12:v=float(w[6][x])/float(w[3][x])
                        else:
                            if x==636:v='3'
                            elif x in [1321,1793]:v='2'
                            elif x in [2941,3415]:v='1'
                            else:v=(float(w[3][x])/(float(w[3][x])-float(w[7][x])))**2
                        v=round(v,int(w[l][x]))
                        if w[l][x]=='0':d+=str(int(v))
                        else:d+=str(v)
                    except:d+=w[l][x]
            if l!=13:d+=';'
        d+='\n'
    d=d.replace(".",",")
    sys.stdout.write(d)
if l==3:
    p=[-1.08589,1365.49,0.016679,64.559187,1.131426,5601.76666,0.033079,-25.24067,-0.302556,-0.706202,57.668242,5.0]
    r=range(256)
    r[210:216]=[347,5578,6625,7898,8650,9622]
    v=[];e=[];c=[];a=10000
    s=b[:a]
    b=b[a:]
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
    i=u[:a]
    d=["{:02d}".format(e)for e in u[a:]]
    r=[float(x+y+"."+z) for x,y,z in zip(["-"if x=='0'else''for x in s],[str(x) for x in i],d)]
    n=t(a)
    r=["{:.2f}".format(round(m(n[x],x,*p),2)+a) for x,a in enumerate(r)] 
    sys.stdout.write("\n".join([i[:-3] if i[-2:]=='00'else (i[:-1] if i[-1]=='0'else i) for i in r])+"\n")
if l==4:
    d='+-1032547698'
    e=('110','100','111','0100','1011','001','1010','0111','0101','0001','0000','0110')
    r=""
    b=b[:-3]
    while len(b)>0:
        i=np.where(map(lambda x:b.startswith(x),e))[0][0]
        r+=d[i]
        b=b[len(e[i]):]
    nums=[int(e) for e in re.findall('[+-]\d+',r)]
    ret=[]
    cur=0
    for e in nums:
        cur+=e
        ret.append(cur)
    sys.stdout.write(struct.pack('1250H',*ret))
    
    
    