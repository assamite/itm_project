import struct,sys
ir=xrange(255)
dr=xrange(100)
def f(path):
    r=reduce(lambda x,y:x+'{:08b}'.format(y),struct.unpack('4000B',open(path).read()),"")
    a=2000
    s=["-" if x=='0' else '' for x in r[:a]]
    i=map(lambda x:str(int("".join(x),2)),zip(*[iter(r[a:a*9])]*8))
    d=map(lambda x:str(int("".join(x),2)),zip(*[iter(r[a*9:])]*7))
    return "\n".join([x+y+"."+z for x,y,z in zip(s,i,d)])+"\n"
