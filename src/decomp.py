import sys,struct
f=open(sys.argv[1]).read()
b=reduce(lambda x,y:x+'{:08b}'.format(y),struct.unpack('{}B'.format(len(f[1:])),f[1:],""))
if f[0]==1:
    m=lambda x:0
    a=2000
    s=["-" if x=='0' else '' for x in b[:a]]
    i=map(lambda x:str(int("".join(x),2)),zip(*[iter(b[a:a*9])]*8))
    d=map(lambda x:str(int("".join(x),2)),zip(*[iter(b[a*9:])]*7))
    sys.stdout.write("\n".join([str(m(i)+x) for i,x in enumerate([float(x+y+"."+z) for x,y,z in zip(s,i,d)])])+"\n")
else:
    sys.stdout.write("Hjaelp! I need to be coded!")