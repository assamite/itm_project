import struct,numpy,re,sys
c='.1032547698'
e=['00','011','1000','1111','010','1001','1100','1010','1011','1110','1101']
bts=reduce(lambda x,y:x+'{:08b}'.format(y),struct.unpack('4881B',open(sys.argv[1]).read()),"")[:-3]
b=bts[:2000]
h=bts[2000:]
s=""
while len(h)>0:
    i=numpy.where(map(lambda x:h.startswith(x),e))[0][0]
    s+=c[i]
    h=h[len(e[i]):]
sys.stdout.write("\n".join(["-"+x if b[i]=='0' else x for i,x in enumerate(re.findall('\d+[.]\d{2}',s))])+"\n")

