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
    k = [83,23899,6800,3094,5143,8943,4270,1365,964,7433]
    o=1
    for x in range(10):
        w.append(bz2.decompress(f[o:o+k[x]]).split(";")[:-1])
        o=o+k[x]
    d=';'.join(w[0])+';WER\n'
    del w[0]
    j=''
    for x in range(4128):
        A=['']*14
        for l in range(14):
            if l in [0,1,3]:
                A[l]=(w[l][x])
            elif l==4:
                A[l]=w[4][2*x]
            elif l==5:
                A[l]=w[4][2*x+1]
            elif l in [6,7]:
                A[l]=(w[l-1][x])
            elif l in [2,9]:
                if l==2:y=0
                else:y=1
                if w[2][2*x+y]=='a':
                    try:A[l]=(str(int(math.ceil(float(w[3][x])))))
                    except:pass
                elif w[2][2*x+y]=='b':A[l]=A[2]
                else: A[l]= w[2][2*x+y]
            elif l==8:
                if w[7][x]=='a':A[l]=j
                else:
                    j=w[7][x]
                    A[l]=j
            elif l in [10,11,12,13]:
                y=l-10
                if w[8][4*x+y]=='b':A[l]='#DIV/0!'
                elif w[8][4*x+y]!='a':
                    try:
                        if l==10:v=float(A[4])/float(A[3])
                        elif l==11:v=float(A[4])/float(A[5])
                        elif l==12:v=float(A[6])/float(A[3])
                        else:
                            if x==636:v='3'
                            elif x in [1321,1793]:v='2'
                            elif x in [2941,3415]:v='1'
                            else:v=(float(A[3])/(float(A[3])-float(A[7])))**2
                        v=round(v,int(w[8][4*x+y]))
                        if w[8][4*x+y]=='0':A[l]=str(int(v))
                        else:A[l]=str(v)
                    except:A[l]=w[8][4*x+y]
        d=d+';'.join(A)
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
if l==5:
    y=400
    d=[0 for r in range(y)]
    d[:2]=[1,3]
    for t in range(2,y):          
        d[t]=d[t-1]+d[t-2]
    b=""
    for t in range(220):
        b+='{:01b}'.format(d[t+80])
    b+='00'
    s=[]
    for i in xrange(0,len(b),8):
        e=b[i:i+8] 
        e=e[5:]+e[:5]
        s.append(int(e,2))
    sys.stdout.write(struct.pack('2700B'.format(),*s[:2700]))