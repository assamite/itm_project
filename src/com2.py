from struct import pack
# Get unsigned integers by moving each integer by the max negative amount.
# This will converted back in the decompressor dec2.py
r = [int(i.strip())+1100 for i in open('../data/curve1.dat','r').read().split()]
bitstring = ""
for c in r:
    # unsigned integer in bit format with possible preceding 0's.
    # Max value for integer is 2**11 -1 (2047)
    bitc = "{0:011b}".format(c)  
    bitstring += bitc
  
bytes = []  
# Read 8 bits a time, convert it to unsigned integer
for i in xrange(0, len(bitstring), 8): 
    by = int(bitstring[i:i+8], 2)
    bytes.append(by)
   
#Write all unsigned integers into a file 
open('test','w').write(pack('{}B'.format(len(bytes)),*bytes))