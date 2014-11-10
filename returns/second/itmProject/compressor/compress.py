import struct, utils,sys
r = [float(i.strip()) for i in open(sys.argv[1]).read().split()]
st = "".join(['0' if i<0 else '1' for i in r])
ar = [abs(i) for i in r]
sar = "".join(['{:.2f}'.format(i) for i in ar])
s, enc = utils.str2encode(sar)
if len(s) % 8 != 8:
    for x in xrange(8 - (len(s) % 8)):
        s += '0'

bitstring = st + s
bts = []
for i in xrange(0, len(bitstring), 8):
    by = int(bitstring[i:i+8], 2)
    bts.append(by)
    
#Write all unsigned integers into a file 
sys.stdout.write(struct.pack('{}B'.format(len(bts)),*bts))