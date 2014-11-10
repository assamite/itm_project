import sys
import struct
import utils
e,b,a=utils.nums2bin([float(i.strip()) for i in open(sys.argv[1]).read().split()])
sys.stdout.write(struct.pack("{}B".format(len(b)), *b))

'''
if len(sys.argv) == 3:
    sf = open(sys.argv[1])    # side info file
    df = open(sys.argv[2])    # data file
elif len(sys.argv) == 2:
    sf = None
    df = open(sys.argv[1])    # data file
else:
    print "usage: " + sys.argv[0] + " [<sdat>] <data>"
    sys.exit(-1)

for line in df:
   sys.stdout.write(line)
'''
