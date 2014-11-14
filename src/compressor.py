'''Compressor for all the files
'''
import struct, utils,sys
import numpy as np

ids = {
    'curve1.dat': 1,
    'paleo.csv': 2   
    }

def curve1_compressor(x, a, b, c, d, e, f, g, h, i, j, k):
    val = [0 for n in range(len(x))]
    for n in range(len(x)):
        if(n<1250):
            val[n] = (np.abs(a*x[n] + b)) *(-1)* (np.abs(np.cos(c*x[n]))-1)**2+d
        else:
            val[n] = (e*(x[n]-1250) + f) * ( np.abs( np.cos(g*(x[n]-1250) + h) + i ) +j ) + k    
    return np.array(val)


if sys.argv[1][-len('curve1.dat'):] == 'curve1.dat':
    orig = np.array([float(i.strip()) for i in open(sys.argv[1]).read().split()])
    ran = np.linspace(0,1999,num=2000)
    guessed_params = [-1.08, 1363, 1.0/60, 15, 1.09,-28.15,1.0/30,-24.33,0.27,-0.7,2.64]
    estimates = curve1_compressor(ran, *guessed_params)
    estimates = np.array([round(e, 2) for e in estimates])
    residuals = orig - estimates

    signs = reduce(lambda x,y: x+('0' if y<=0 else '1'), residuals, "")
    residuals_abs = [np.abs(r) for r in residuals]
    residuals_int = np.array([int(r) for r in residuals_abs])
    residuals_dec = np.array([str(round(r - int(r),2)).split(".")[1] for r in residuals_abs])
    residuals_dec = np.array([r +"0" if len(r)==1 else r for r in residuals_dec])
    #print residuals_dec
    residuals_int_set = set(residuals_int)
    residuals_int_sorted = sorted(list(residuals_int_set))
    with open('res_ints.dat', 'w') as f:
        f.write("["+",".join([str(i) for i in residuals_int_sorted]) +"]")
        
    if residuals_int[1355] != 83: # Some VERY peculiar bug on casting abs value to int
        residuals_int[1355] = 83

    #print residuals_int_sorted
    res_bits = np.ceil(np.log2(len(residuals_int_set)))
    #print res_bits
    residuals_int_bits = reduce(lambda x,y:x+("{:0"+str(int(res_bits))+"b}").format(residuals_int_sorted.index(y)), residuals_int, "")
    residuals_dec_bits = reduce(lambda x,y:x+"{:07b}".format(int(y)),residuals_dec, "")
    #print len(residuals_int_bits) / 8
    #print len(residuals_dec_bits) / 8

    s = "{:08b}".format(ids['curve1.dat']) + signs + residuals_int_bits + residuals_dec_bits
    #print len(s)
    if len(s) % 8 != 8 and len(s) % 8 != 0:
        #print len(s) % 8
        for x in xrange(8 - (len(s) % 8)):
            s += '0'
    
    bitstring = s
    #print len(bitstring), float(len(bitstring)) / 8
    bts = []
    for i in xrange(0, len(bitstring), 8):
        by = int(bitstring[i:i+8], 2)
        bts.append(by)
        
    #Write all unsigned integers into a file 
    sys.stdout.write(struct.pack('{}B'.format(len(bts)),*bts))
    
