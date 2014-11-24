def g(h):
    return str(int(math.ceil(float(r[h]))))
import math, numpy
d=open("c","r").read().split("\n")[:-1]
o=[]
o.append(d[0])
del d[0]
b=0
for i in range(len(d)):
    r=d[i].split(";")
    l=''
    for j in range(len(r)-1):
        a=r[j]
        if j==2 or j==9:
            if a=='-1':
                if r[3]!='':l+=g(3)
            elif a=='-2':
                if r[2]!='':l+=g(2)
            else:l+=a
        elif j==8:
            if a=='a':l+=b
            else:
                l+=a
                b=a
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
        else: l+=a
        l+=';'
    o.append(l.replace(".",",")[:-1])
numpy.savetxt("pal",o,'%s')
