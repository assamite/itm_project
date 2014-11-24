'''Playing with group.stock.dat (the 2500B one)
'''
import re
import sys
import struct
import utils
import numpy as np
from matplotlib import pyplot as plt

# Seems like h/H is way to go with this data.
stock = struct.unpack('1250H', open('../data/group.stock.dat').read())
#print stock
#plt.plot(stock)
#plt.show()

# Diffs from index to next
diffs = [stock[0]]
for i,s in enumerate(stock[1:]):
    diffs.append(s-stock[i])
  
plt.plot(diffs[2:])
plt.show()

enc, bts, a = utils.nums2bin(diffs,'stock.test')
print len(bts)
print enc
print a
b=reduce(lambda x,y:x+'{:08b}'.format(y),struct.unpack("{}B".format(len(bts)),open('stock.test').read()),"")[:-a]

d='+-1032547698'
e=('110','100','111','0100','1011','001','1010','0111','0101','0001','0000','0110')
r=""
while len(b)>0:
    i=np.where(map(lambda x:b.startswith(x),e))[0][0]
    r+=d[i]
    b=b[len(e[i]):]
nums = [int(e) for e in re.findall('[+-]\d+',r)]
print nums
ret=[]
cur=0
for e in nums:
    cur+=e
    ret.append(cur)
print ret
with open('stock.test.decom','w') as f:
    f.write(struct.pack('1250H',*ret))
