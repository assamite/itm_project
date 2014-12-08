'''Compressor for all the files
'''
import struct,utils,sys,gzip
import numpy as np
import math, bz2

ids = {
    'curve1.dat': 1,
    'paleo.csv': 2,
    'ty.txt': 3,  
    'group.stock.dat': 4,
    'monty_python_data_1.dat': 5,
    'caravan.dat': 6,
    'final.dat': 7
    }

def curve1_compressor(x, a, b, c, d, e, f, g, h, i, j, k, multiplier):
    val = [0 for n in range(len(x))]
    for n in range(len(x)):
        if(n<1250*multiplier):
            val[n] = (np.abs(a*x[n] + b)) *(-1)* (np.abs(np.cos(c*x[n]))-1)**2+d
        else:
            val[n] = (e*(x[n]-(1250*multiplier)) + f) * ( np.abs( np.cos(g*(x[n]-(1250*multiplier)) + h) + i ) +j ) + k
    return np.array(val)


def poly55(x,y,p00,p10,p01,p20,p11,p02,p30,p21,p12,p03,p40,p31,p22,p13,p04,p50,p41,p32,p23,p14,p05):
    return p00 + p10*x + p01*y + p20*x**2 + p11*x*y + p02*y**2 + p30*x**3 +\
        p21*x**2*y + p12*x*y**2 + p03*y**3 + p40*x**4 + p31*x**3*y +\
        p22*x**2*y**2 + p13*x*y**3 + p04*y**4 + p50*x**5 + p41*x**4*y +\
        p32*x**3*y**2 + p23*x**2*y**3 + p14*x*y**4 + p05*y**5
        
def poly2(x,p1,p2,p3):
    return p1*x**2 + p2*x + p3

if sys.argv[1][-len('curve1.dat'):] == 'curve1.dat':
    orig = np.array([float(i.strip()) for i in open(sys.argv[1]).read().split()])
    ran = np.linspace(0,1999,num=2000)
    p = [-1.08, 1363, 1.0/60, 15, 1.09,-28.15,1.0/30,-24.33,0.27,-0.7,2.64, 1]
    estimates = curve1_compressor(ran, *p)
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
    residual_mappings = range(256)
    residual_mappings[210:213] = [256,276,342]
        
    if residuals_int[1355] != 83: # Some VERY peculiar bug on casting abs value to int
        residuals_int[1355] = 83

    #print residuals_int_sorted
    res_bits = np.ceil(np.log2(len(residuals_int_set)))
    #print res_bits
    residuals_int_bits = reduce(lambda x,y:x+("{:0"+str(int(res_bits))+"b}").format(residual_mappings.index(y)), residuals_int, "")
    residuals_dec_bits = reduce(lambda x,y:x+"{:07b}".format(int(y)),residuals_dec, "")
    #print len(residuals_int_bits) / 8
    #print len(residuals_dec_bits) / 8

    s = "{0:08b}".format(ids['curve1.dat']) + signs + residuals_int_bits + residuals_dec_bits
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
    

if sys.argv[1][-len('ty.txt'):] == 'ty.txt':
    orig = np.array([float(i.strip()) for i in open(sys.argv[1]).read().split()])
    ran = np.linspace(0,1999,num=10000)
    p = [-1.08589, 1365.49, 0.016679, 58.559187,1.131426,5601.76666,0.033079,-25.24067,-0.302556,-0.706202,51.668242,5]
    estimates = curve1_compressor(ran, *p)
    estimates = np.array([round(e, 2) for e in estimates])
    residuals = orig - estimates

    signs = reduce(lambda x,y: x+('0' if y<=0 else '1'), residuals, "")
    residuals_abs = [np.abs(r) for r in residuals]
    residuals_int = [int(r) for r in residuals_abs]
    residuals_dec = np.array([str(round(r - int(r),2)).split(".")[1] for r in residuals_abs])
    residuals_dec = [r +"0" if len(r)==1 else r for r in residuals_dec]
    residuals_int_set = set(residuals_int)
    residuals_int_sorted = sorted(list(residuals_int_set))
    #print len(residuals_int_sorted)
    
    residual_mappings = range(256)
    residual_mappings[210:216] = [353, 5584, 6631, 7904, 8656, 9628]
    '''  
    for i in xrange(len(residuals_int)):
        if int(residuals_abs[i]) != residuals_int[i]:
            print i, residuals_abs[i], residuals_int[i]
    ''' 
    anomalies = [1323,1777, 4337,9563]
    # Uhh, where do these come from?
    residuals_int[1323] += 1
    residuals_int[1777] += 1
    residuals_int[4337] += 1
    residuals_int[9563] += 1
    
    
    residuals_int_mapped = map(lambda x: residual_mappings.index(x), residuals_int)
    residuals_dec_mapped = map(lambda x: residual_mappings.index(int(x)), residuals_dec)
    residuals_all = residuals_int_mapped + residuals_dec_mapped
    #print len(residuals_all)
    #np.savetxt("res_all",residuals_all,"%s")
    
    enc, a1, s, a2 = utils.ints2hfbin(residuals_all, filepath = 'tyhf.test')
    #print a1, a2
    #print len(s), len(s) / 8.0
    #print len(s) / 8.0, len(signs) / 8.0
    s = "{0:08b}".format(ids['ty.txt']) + signs + enc + s
    if len(s) % 8 != 8 and len(s) % 8 != 0:
        #print len(s) % 8
        for x in xrange(8 - (len(s) % 8)):
            s += '0'
    
    bitstring = s
    bts = []
    for i in xrange(0, len(bitstring), 8):
        by = int(bitstring[i:i+8], 2)
        bts.append(by)
      
    #print len(bts), a1, a2 
    #Write all unsigned integers into a file 
    sys.stdout.write(struct.pack('{}B'.format(len(bts)),*bts))
    

if sys.argv[1][-len('group.stock.dat'):] == 'group.stock.dat':
    stock = struct.unpack('1250H', open(sys.argv[1]).read())
    diffs = [stock[0]]
    for i,s in enumerate(stock[1:]):
        diffs.append(s-stock[i])
    enc, bts, a = utils.nums2bin(diffs)
    bts = [ids['group.stock.dat']] + bts
    sys.stdout.write(struct.pack('{}B'.format(len(bts)), *bts))

if sys.argv[1][-len('paleo.csv'):] == 'paleo.csv':
    data=open(sys.argv[1]).read().split("\n")[:-1]
    strings=['','','','','','','','','','','','','','','']
    strings[14]+=data[0]
    data = [x.replace(",",".") for x in data[1:]]
    previouslobes=0
    for i in range(len(data)):
        record = data[i].split(";")
        # Field name - no specific implementation yet
        strings[0] += record[0]

        # Field ??? - no specific implementation yet
        strings[1] += record[1]

        # Field maxdm(1) - Replace values that equal ceil(dm) with marker 'a'. Otherwise original values.
        try:dm = str(int(math.ceil((float(record[3])))))
        except: dm=''
        if record[2] == dm:strings[2] += 'a'
        else: strings[2] += record[2]

        # Fields dm, ww, wh, uw, ah - no specific implementation yet
        for j in range(3,8):
            strings[j] += record[j]

        # Field lobes - Replace values that equal that of the previous record with marker 'a'. Otherwise original values.
        if record[8] == previouslobes: strings[8] += 'a'
        else:
            strings[8] += record[8]
            previouslobes = record[8]

        # Field maxdm(2) - Replace values that equal ceil(dm) with marker 'a', and those that equal maxdm(1) with marker
        # 'b'. Otherwise original values.
        if record[9] == dm: strings[9] += 'a'
        elif record[9] == record[2]: strings[9] += 'b'
        else: strings[9] += record[9]

        # Fields ww/dm, ww/wh, uw/dm, WER ((dm/(dm-ah)^2) - Values replaced as follows:
        # Integer value 0-9:    The accuracy of the field (the length of the decimal part), if
        #                       the field can be generated by the calculation in the name of the field
        # 'a':                  If the field is empty ('')
        # 'b':                  If the field contains a 'division by zero'-error marker '#DIV/0!'
        # Original value:       Otherwise (field contains some value, but it seems arbitrary)

        for j in range(10,14):
            if record[j] == '': strings[j] += 'a'
            elif record[j] == '#DIV/0!': strings[j] += 'b'
            else:
                try: accuracy = len(record[j].split(".")[1])
                except: accuracy = 0
                if j==10:
                    try:
                        if float(record[10]) == round(float(record[4])/float(record[3]),accuracy):
                            strings[j] += str(accuracy)
                        else: strings[j] += record[10]
                    except: strings[j] += record[10]

                elif j==11:
                    try:
                        if float(record[11]) == round(float(record[4])/float(record[5]),accuracy):
                            strings[j] += str(accuracy)
                        else: strings[j] += record[11]
                    except: strings[j] += record[11]
                elif j==12:
                    try:
                        if float(record[12]) == round(float(record[6])/float(record[3]),accuracy):
                            strings[j] += str(accuracy)
                        else:
                            strings[j] += record[12]
                    except:
                        strings[j] += record[12]
                elif j==13:
                    try:
                        if float(record[13]) == round((float(record[3])/(float(record[3])-float(record[7])))**2,accuracy):
                            strings[j] += str(accuracy)
                        else: strings[j] += record[13]
                    except: strings[j] += record[13]


        # Adding delimiters between values
        for j in range(len(strings))[:-1]:
            strings[j] += ';'

    # Compress column by column with bzip2 and concatenate the resulting bitstrings
    bits=bz2.compress(strings[14])
    for x in range(len(strings))[:-1]:
        bit = bz2.compress(strings[x])
        bits += bit
    bits = struct.pack('B',2)+bits
    sys.stdout.write(bits)

if sys.argv[1][-len('monty_python_data_1.dat'):] == 'monty_python_data_1.dat':
    b = "{:08b}".format(ids['monty_python_data_1.dat'])
    bts = [int(b, 2)]
    sys.stdout.write(struct.pack('1B', *bts))
    
    
if sys.argv[1][-len('final.sdat'):] == 'final.sdat':
    a=np.array([[float(i) for i in e.split()] for e in open(sys.argv[1]).read().split("\n")[:-1]])
    Y=a[:,0]
    Z=a[:,1]
    #for s in sdat:
    #    l = s.split(" ")
    #    Y.append(float(l[0]))
    #    Z.append(float(l[1]))
    Y = np.array(Y)
    Z = np.array(Z)
    X = np.array([float(x) for x in open(sys.argv[2]).read().split()])
    #print Y.shape, Z.shape, X.shape
    indeces = np.zeros(X.shape)
    p2coef = [0.7028,2.771,-6.879]
    p50coef = [-18.290171,1.221760,9.672956,0.593337,0.930333,-0.857963,0.081794,0.110596,-0.004892,0.202391,-0.006623,-0.024314,-0.004627,0.007206,-0.035267,-0.001812,0.002337,-0.002610,0.006790,0.014688,-0.165668]
    p51coef = [3.129242,2.742070,-5.965026,0.843920,-0.488139,-1.651493,0.034052,-0.089867,0.215533,0.089603,-0.004858,0.005126,0.029028,0.145531,0.056595,-0.001043,0.000423,0.002002,0.014120,0.013710,0.005316]
    
    # Choose with model to use for each data point by check is the data point under or above the curve.
    for i,e in enumerate(indeces):
        if poly2(Y[i],*p2coef) < X[i]:
            indeces[i] = 1
            
    # Calculate residuals based on the model
    residuals = np.zeros(X.shape)
    for i,r in enumerate(residuals):
        y = Y[i]
        z = Z[i]
        if indeces[i] == 1:
            surface = poly55(y,z,*p51coef)
        else:
            surface = poly55(y,z,*p50coef)
        res = X[i] - surface
        residuals[i] = round(res, 3)
    
    ires = [(str(int(i)) if i<0 else '+'+str(int(i))) if int(i)!=0 else ('-0' if i<0 else '+0') for i in residuals]
    #print ires[:10], set(ires)
    iires = ['-'+e if indeces[i]==0 else '+'+e for i,e in enumerate(ires)]
    ind = sorted(list(set(iires)))
    #print ind, set(iires)
    iiires = [ind.index(i) for i in iires]
    enchf, a1, ihf, a2 = utils.ints2hfbin(iiires) 
    #print len(enchf) / 8.0, len(ihf) / 8.0
    #print (len(enchf) + len(ihf)) / 8.0
    #print a1, a2
    
    ares = np.array([str(round(abs(r) - abs(int(r)),3)).split(".")[1] for r in residuals])
    dres = [r if len(r)==3 else (r+"0" if len(r)==2 else r+"00") for r in ares]
    #print dres[:20]
    #for d in dres:
    #    if len(d) != 3:
    #        print d
            
    sdres = reduce(lambda x,y: x + y, dres, "")
    #print len(sdres)
    hf, enc = utils.str2encode(sdres)
    #print len(hf) / 8.0
    if len(hf) % 8 != 0:
        a3 = 8 - len(hf) % 8
        for i in xrange(a3):
            hf += '0'
            
   # print len(hf) / 8.0, a3
    
    denc = {}
    for k,v in enc.items():
        denc[int(k)] = v

    denchf, a4 = utils.hf2bin256(denc)
    #print denc
    #print len(denchf) / 8.0, a4
    bitstring = "{:08b}".format(ids['final.dat']) + enchf + ihf + denchf + hf
    bts = []
    for i in xrange(0, len(bitstring), 8):
        by = int(bitstring[i:i+8], 2)
        bts.append(by) 
    
    sys.stdout.write(struct.pack('{}B'.format(len(bts)),*bts))
    
    
