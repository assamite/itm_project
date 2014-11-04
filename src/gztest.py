import gzip
open('curve1.dat','w').write(gzip.open('../test/curve1.dat.gz','r').read())
