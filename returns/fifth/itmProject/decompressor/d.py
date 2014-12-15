import sys,struct,re,numpy as np,math,bz2
if len(sys.argv)==2:
    f=open(sys.argv[1]).read()
else:
    f=open(sys.argv[2]).read() 
    g=open(sys.argv[1]).read()
b=reduce(lambda x,y:x+'{:08b}'.format(y),struct.unpack('{}B'.format(len(f)),f),"")
l=int(b[:8],2)
b=b[8:]
t=lambda x:np.linspace(0,1999,x)
def m(n,y,a,b,c,d,e,f,g,h,i,j,k,x):
    if(y<1250*x):
        return (-1*np.abs(a*n+b))*(np.abs(np.cos(c*n))-1)**2+d
    else:
        return (e*(n-1250*x)+f)*(np.abs(np.cos(g*(n-1250*x)+h)+i)+j)+k
def p(x,y,p00,p10,p01,p20,p11,p02,p30,p21,p12,p03,p40,p31,p22,p13,p04,p50,p41,p32,p23,p14,p05):
    return p00 + p10*x + p01*y + p20*x**2 + p11*x*y + p02*y**2 + p30*x**3 +\
        p21*x**2*y + p12*x*y**2 + p03*y**3 + p40*x**4 + p31*x**3*y +\
        p22*x**2*y**2 + p13*x*y**3 + p04*y**4 + p50*x**5 + p41*x**4*y +\
        p32*x**3*y**2 + p23*x**2*y**3 + p14*x*y**4 + p05*y**5
def h(b,a,r,d,w,q):
    c=[];e=[];v=[]
    l=int(b[:8],2)
    b=b[8:]
    for i in xrange(l):
        c.append(int(b[:8],2))
        b=b[8:]
        v.append(int(b[:d],2)+1)
        b=b[d:]
    for i in xrange(l):
        e.append(b[:v[i]])
        b=b[v[i]:]
    b=b[w:]
    u=[]
    for i in xrange(a):
        i=np.where(map(lambda x:b.startswith(x),e))[0][0]  
        u.append(r[c[i]])
        b=b[len(e[i]):]
    b=b[q:]
    return u,b
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
    p=[-1.08589,1365.49,0.016679,58.559187,1.131426,5601.76666,0.033079,-25.24067,-0.302556,-0.706202,51.668242,5.0]
    r=range(256)
    r[210:216]=[353, 5584, 6631, 7904, 8656, 9628]
    v=[];e=[];c=[];a=10000
    s=b[:a]
    b=b[a:]
    u,b=h(b,a*2,r,4,4,5)
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
if l in [5,8]:
    if l==5:a=5;A=80;c='2700B';C=2700
    else:a=6;A=90;c='3200B';C=3200
    y=400
    d=[0 for r in range(y)]
    d[:2]=[1,3]
    for t in range(2,y):
        d[t]=d[t-1]+d[t-2]
    b=""
    for t in range(220):
        b+='{:01b}'.format(d[t+A])
    if l==5:b+='00'
    s=[]
    for i in xrange(0,len(b),8):
        e=b[i:i+8]
        e=e[a:]+e[:a]
        s.append(int(e,2))
    sys.stdout.write(struct.pack(c.format(),*s[:C]))
if l==7:
    s=np.array([[float(i) for i in e.split()] for e in g.split("\n")[:-1]])
    Y=s[:,0]
    Z=s[:,1]
    c=[-18.290171,1.221760,9.672956,0.593337,0.930333,-0.857963,0.081794,0.110596,-0.004892,0.202391,-0.006623,-0.024314,-0.004627,0.007206,-0.035267,-0.001812,0.002337,-0.002610,0.006790,0.014688,-0.165668]
    d=[3.129242,2.742070,-5.965026,0.843920,-0.488139,-1.651493,0.034052,-0.089867,0.215533,0.089603,-0.004858,0.005126,0.029028,0.145531,0.056595,-0.001043,0.000423,0.002002,0.014120,0.013710,0.005316]
    a=20000
    r=['++0','++1','++2','++3','+-0','+-1','+-2','+-3','-+0','-+1','--0','--1']
    u,w=h(b,a,r,4,7,5)
    r='0123456789'
    v,q=h(w,a*3,r,2,2,3)
    m=[e[0] for e in u]
    s=[e[1] for e in u]
    n=[e[2] for e in u]
    t=[float(n[i]+"."+e) for i,e in enumerate(map(lambda x:"".join(x),zip(*[iter(v)]*3)))]
    S=[p(e[0],e[1],*c) if m[i]=='-' else p(e[0],e[1],*d) for i,e in enumerate(zip(Y,Z))]
    S=[round(e,3) for e in S]
    X=[e+t[i] if s[i]=='+' else e-t[i] for i,e in enumerate(S)]
    X=[round(e,3) for e in X]
    X=[int(e) if int(e)==e else e for e in X]
    sys.stdout.write("\n".join([str(x) for x in X])+"\n")