import sys,struct,numpy,re
e=('0101','000','111','0100','001','1101','1100','1001','0110','1000','0111','1010','1011')
c="+-.0123456789"
h=reduce(lambda x,y:x+'{:08b}'.format(y),struct.unpack('5742B',open(sys.argv[1]).read()),"")[:-4]
s=""
while len(h)>0:
    i=numpy.where(map(lambda x:h.startswith(x),e))[0][0]
    s+=c[i]
    h=h[len(e[i]):]
sys.stdout.write("\n".join(["{:.2f}".format(float(x)) for x in re.findall('[+-]\d+[.]\d+',s)])+"\n")


