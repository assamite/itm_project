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
    firstline=data[0]
    del data[0]
    data=[x.replace(",",".") for x in data]

    # The next part generates array 'accuracy' It contains the length of the decimal part for the entries in fields
    # 10,...,13, in the case where the result can be calculated from the values in fields dm,ah,wh,ww and uw. Negative
    # special values are reserved for abnormal values,  -1 = ''(empty field), -2 = '#DIV/0!'.
    # In the case where the value of a field cannot be correctly deduced from the fields ww,wh,ah,dm,uw, the
    # corresponding field in 'accuracy' contains the original value from the data

    accuracy = []
    for i in range(len(data)):
        row=[0,0,0,0] # 'row' contains 'accuracy' values of a single record, appended later to 'accuracy'
        record = data[i].split(";")
        for indx in range(0,4):
            if record[10+indx]=='':
                row[indx]=-1
            elif record[10+indx]=='#DIV/0!':
                row[indx]=-2
            else:
                temp = record[10+indx].split(".")
                if len(temp)==2:
                    row[indx]=len(temp[1])

        for k in range(1,len(record)):
            if record[k]=='' or record[k]=='#DIV/0!':
                record[k]='0'
            record[k]=float(record[k])

        if record[3]==0:
            if record[10]!=0 and row[0]>=0:
                row[0]=record[10]
            if record[12]!=0 and row[2]>=0:
                row[2]=record[12]
        else:
            if record[10] != round(record[4]/record[3], row[0]) and row[0]>=0:
                row[0]=record[10]
            if record[12] != round(record[6]/record[3], row[2]) and row[2]>=0:
                row[2]=record[12]
        if record[5]==0:
            if record[11]!=0 and row[1]>=0:
                row[1]=record[11]
        elif record[11] != round(record[4]/record[5], row[1]) and row[1] >=0:
            row[1]=record[11]
        if(record[3]-record[7]==0) and row[3]>=0:
            row[3]=record[13]
        elif row[3]>=0 and record[13] != round((record[3]/(record[3]-record[7]))**2,row[3]):
            row[3]=record[13]
        row = [str(x) for x in row]
        accuracy.append(row)

    # Now, we do a similar trick to the three diameter fields. The two maxdm-fields are often deducible by rounding the
    # dm value up to the next integer. Also, the second maxdm is often the same as the first. maxdm1 and maxdm2 contain
    # the values of the first and second maxdm fields, with values in both replaced by '-1' if the original value equals
    # the dm-field rounded up. '-2' marks the case where the second maxdm doesn't equal round(dm), but equals the first maxdm

    maxdm1 = []
    maxdm2 = []
    for i in range(len(data)):
        record=data[i].split(";")
        try:dm = str(int(math.ceil((float(record[3])))))
        except: dm=''
        if record[2] == dm:
            maxdm1.append(-1)
        else:
            maxdm1.append(record[2])
        if record[9] == dm:
            maxdm2.append(-1)
        elif record[9]==record[2]:
            maxdm2.append(-2)
        else:
            maxdm2.append(record[9])

    # The value of the lobes field is often the same in consecutive records. We save a little space (approx 1k after
    # bzip) by replacing the value with 'a' if the lobes value of a record is the same as that of the previous record.

    lobes=[]
    for i in reversed(range(len(data))[1:]):
        record=data[i].split(";")
        record2=data[i-1].split(";")
        if record[8]==record2[8]:
            lobes.append('a')
        else:
            lobes.append(record[8])
    lobes.append(data[0].split(";")[8])

    # Now, we just need to generate the new data, with the values replaced by the ones we just calculated.
    newdata=[]
    newstring=firstline+'\n'
    newdata.append(firstline)
    for i in range(len(data)):
        newrecord=''
        record = data[i].split(";")
        for j in range(len(record)):
            if j!= 2 and j!=8 and j!=9 and j!=10 and j!=11 and j!=12 and j!=13:
                newrecord += (record[j]+';')
            elif j==2:
                newrecord += (str(maxdm1[i])+';')
            elif j==8:
                newrecord += lobes[len(data)-i-1]+';'
            elif j==9:
                newrecord += (str(maxdm2[i])+';')
            elif j==10:
                newrecord += (str(accuracy[i][0])+';')
            elif j==11:
                newrecord += (str(accuracy[i][1])+';')
            elif j==12:
                newrecord += (str(accuracy[i][2])+';')
            else:
                newrecord += (str(accuracy[i][3])+';')
        newdata.append(newrecord)
        newstring+=newrecord+'\n'
    bits=bz2.compress(newstring)
    bits = struct.pack('B',2)+bits
    #bits = struct.pack("{0:08b}".format(ids['paleo.csv']))+bits
    #bits = struct.pack("{0:08b}",ids['paleo.csv'])+bits
    sys.stdout.write(bits)
    
