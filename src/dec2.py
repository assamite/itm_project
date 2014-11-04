from struct import unpack
open('curve1.dat','w').write("\n".join([str(int(i,2)-1100) for i in map("".join,zip(*[iter(bin(reduce(lambda x,y:(x<<8)+y,unpack('275B',open('test','r').read())))[2:])]*11))])+"\n")
