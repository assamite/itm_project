from struct import unpack
open('curve1.dat', 'w').write("\n".join([str(e-1100) for e in unpack('200h',open('../test/c','r').read())]) + "\n")
