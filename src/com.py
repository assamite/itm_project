from struct import pack
r = [int(i.strip())+1100 for i in open('../data/curve1.dat','r').read().split()]
open('../test/c','w').write(pack('200h',*r))