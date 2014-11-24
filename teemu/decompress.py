__author__ = 'teemupitkanen1'
def g(h):
    return str(int(math.ceil(float(r[h]))))
import math, numpy
d=open("c","r").read().split("\n")
d.pop()
f=d[0]
del d[0]
o=[]
o.append(f)
for i in range(len(d)):
    r=d[i].split(";")
    l=''
    for j in range(len(r)-1):
        a=r[j]
        if j==2:
            if a=='-1':
                if r[3]!='':l+=g(3)
            else:l+=a
        elif j==9:
            if r[3]!='' and a=='-1':l+=g(3)
            elif r[2]!='' and a=='-2':l+=g(2)
            else:l+=a
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
        if j!=13:l+=';'
       # if i==3880:l='kangastus tuominen;1453;;;;;;;;;;;;'
    o.append(l.replace(".",","))
numpy.savetxt("pal",o,'%s')
