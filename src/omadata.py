'''Squeezing the size of our own data.
'''
import struct,numpy as np
y=400
d=[0 for r in range(y)]
d[:2]=[1,3]
for t in range(2,y):          
    d[t]=d[t-1]+d[t-2]
b=""
for t in range(220):
    b+='{:01b}'.format(d[t+80])
b+='00'
s=[]
for i in xrange(0,len(b),8):
    e=b[i:i+8] 
    e=e[5:]+e[:5]
    s.append(int(e,2))
sys.stdout.write(struct.pack('2700B'.format(),*s[:2700]))
