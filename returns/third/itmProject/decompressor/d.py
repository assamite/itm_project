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
    d=bz2.decompress(f[1:])[:-1].split("\n") ##!!!!
    d=[str(x) for x in d]
    o=[]
    o.append(d[0])
    del d[0]
    z='0'
    for i in range(len(d)):
        r=d[i].split(";")
        l=''
        for j in range(len(r)-1):
            a=r[j]
            if j==2 or j==9:
                if a=='-1':
                    if r[3]!='':l+=str(int(math.ceil(float(r[3]))))
                elif a=='-2':
                    if r[2]!='':l+=str(int(math.ceil(float(r[2]))))
                else:l+=a
            elif j==8:
                if a=='a':l+=z
                else:
                    l+=a
                    z=a
            elif j in range(10,13):
                if a=='-2':
                    l+='#DIV/0!'
                elif a!='-1':
                    try:
                        b=int(a)
                        if j==10:v=float(r[4])/float(r[3])
                        elif j==11:v=float(r[4])/float(r[5])
                        else:v=float(r[6])/float(r[3])
                        v=round(v,b)
                        if b==0:l+=str(int(v))
                        else: l+=str(v)
                    except:
                        l+=a
            elif j==13:
                if a=='-2':
                    l+='#DIV/0!'
                elif i==636:l+='3'
                elif i==1321:l+='2'
                elif i==1793:l+='2'
                elif i==2941:l+='1'
                elif i==3415:l+='1'
                elif a!='-1':
                    try:
                        b=int(a)
                        v=round((float(r[3])/(float(r[3])-float(r[7])))**2,b)
                        if b==0:
                            v=int(v)
                        l+=str(v)
                    except:
                        l+=a
            else: l+=a
            l+=';'
        o.append(l.replace(".",",")[:-1])
    sys.stdout.write("\n".join([x for x in o])+"\n")
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
    
    
    