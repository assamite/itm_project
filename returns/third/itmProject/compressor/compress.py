'''Compressor for all the files
'''
import struct,utils,sys,gzip
import numpy as np
import math, bz2

ids = {
    'curve1.dat': 1,
    'paleo.csv': 2,
    'ty.txt': 3,  
    'group.stock.dat': 4
    }

def curve1_compressor(x, a, b, c, d, e, f, g, h, i, j, k, multiplier):
    val = [0 for n in range(len(x))]
    for n in range(len(x)):
        if(n<1250*multiplier):
            val[n] = (np.abs(a*x[n] + b)) *(-1)* (np.abs(np.cos(c*x[n]))-1)**2+d
        else:
            val[n] = (e*(x[n]-(1250*multiplier)) + f) * ( np.abs( np.cos(g*(x[n]-(1250*multiplier)) + h) + i ) +j ) + k    
    return np.array(val)


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
    p = [-1.08589, 1365.49, 0.016679, 64.559187,1.131426,5601.76666,0.033079,-25.24067,-0.302556,-0.706202,57.668242,5]
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
    
    residual_mappings = range(256)
    residual_mappings[210:216] = [347,5578,6625,7898,8650,9622]
       
    anomalies = [1323,1777,1827,4337,6250,6251,6252,9563]
    # Uhh, where do these come from?
    residuals_int[1323] = 82
    residuals_int[1777] = 14
    residuals_int[1827] = 29
    residuals_int[4337] = 33
    residuals_int[9563] = 134
    
    residuals_int_mapped = map(lambda x: residual_mappings.index(x), residuals_int)
    residuals_dec_mapped = map(lambda x: residual_mappings.index(int(x)), residuals_dec)
    residuals_all = residuals_int_mapped + residuals_dec_mapped
    #print len(residuals_all)
    
    enc, a1, s, a2 = utils.ints2hfbin(residuals_all)
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
        
    with open('../ty.size', 'w') as f:
        f.write(str(len(bts)))
      
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