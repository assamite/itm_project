'''Various utility functions
'''
from collections import Counter
from heapq import heappush, heappop, heapify
from struct import pack, unpack
import numpy as np
import re

def count_chars(s):
    '''Count number of occurences of each char in str s'''
    return Counter(s)


def count_digits(iterable, unsign = True, split=""):
    """Count number of each digit (and minus symbols) in iterable consisting of 
    integers. If unsign is True, will first make all integers unsigned by adding 
    -min(iterable) to each element. Adds split-string between each integer 
    before passing it to count_chars.
    
    Returns both, the constructed string by concatenating (accorcing to given
    parameters) each integer and the individual character counts.
    """
    add = -int(min(iterable)) if unsign else 0
    digits = reduce(lambda x,y: x+split+str(int(y)+add), iterable, "").strip()
    return digits, count_chars(digits)


def digits2encode(iterable, unsign = True, split = ""):
    '''Get Huffman encoding of the given iterable of integers and the encoded
    binary string.'''
    s, counts = count_digits(iterable, unsign, split)
    enc = _encode2dict(encode(counts))
    return reduce(lambda x,y: x+enc[y], s, ""), enc


def str2encode(s):
    '''Get Huffman encoding of the given str and the encoded binary string.'''
    counts = count_chars(s)
    enc = _encode2dict(encode(counts))
    return reduce(lambda x,y: x+enc[y], s, ""), enc
    
    
def dig2enc(iterable):
    '''Get Huffman encoding of the given iterable of numbers and the encoded
    binary string. TEST version.'''
    digits = reduce(lambda x,y: x+(str(y) if y < 0 else "+"+str(y)), iterable, "").strip()
    counts = count_chars(digits)
    enc = _encode2dict(encode(counts))
    return reduce(lambda x,y: x+enc[y], digits, ""), enc, digits


def nums2bin(iterable, filepath=None):
    '''Convert iterable of numbers to bytes than contain Huffman coded binary 
    string and optionally save it to a file.
    
    Returns Huffman codes, bytes, and amount of zero bits appended to the end to
    get last byte full.
    '''
    huff, enc, digits = dig2enc(iterable)
    add =  8 - (len(huff) % 8) if len(huff) % 8 != 8 else 0
    if add != 0 and add != 8:
        for i in xrange(add): huff += '0'
        
    bts = []  
    # Read 8 bits a time, convert it to unsigned integer
    for i in xrange(0, len(huff), 8): 
        by = int(huff[i:i+8], 2)
        bts.append(by)
    
    if filepath is not None:
        with open(filepath,'w') as f:
            f.write(pack('{}B'.format(len(bts)),*bts))
            
    return enc, bts, add


def bin2str(filepath, enc, nbts, add):
    '''Convert Huffman coded binary file into readable format.
    
    Args:
        filepath: path to binary file
        enc: Huffman code mappings key:char, value:encoding
        bts: number of bytes in binary file
        add: number of zero bits appended to end of the file to get full bytes   
    '''
    # Get bytes and concatenate their binary representations
    bts = unpack('{}B'.format(nbts), open(filepath,'r').read())
    huff_bin = reduce(lambda x,y: x+'{:08b}'.format(y), bts, "")
    if add != 0 and add != 8: # Remove extra bits
        huff_bin = huff_bin[:-add]
    huff_s = ""
    it = enc.items()
    while len(huff_bin) > 0:
        # Get the index of the encoding which appears at the start of the Huffman binary
        i = np.where(map(lambda x: huff_bin.startswith(x[1]), it))[0][0]
        # Add character corresponding to the encoding 
        huff_s += it[i][0]
        # Remove encoding at the start of Huffman binary.
        huff_bin = huff_bin[len(it[i][1]):]
    return huff_s
        
        
def bin2nums(filepath, enc, bts, add):
    '''Convert Huffman coded binary file into number list.
    '''
    hf = bin2str(filepath, enc, bts, add)
    return [float(x) for x in re.findall('[+-]\d+[.]\d+', hf)]


def ints2hfbin(iterable, filepath = None):
    '''Convert iterable of integers into Huffman encoded string, where each 
    integer is converted into its own code word. The resulting Huffman coding
    is added into the start of the binary. 
    '''
    ctr = Counter(iterable)
    enc = _encode2dict(encode(ctr))
    #print max([len(e) for e in enc.values()])
    # Encode the Huffman coding into binary
    encbin, add1 = hf2bin256(enc)
    s = reduce(lambda x,y: x+enc[y],iterable, "")
    
    add2 = len(s) % 8
    if add2 != 0:
        add2 = 8 - add2
        for i in xrange(add2):
            s += "0"
            
    if filepath is not None:
        bts = []
        # Read 8 bits a time, convert it to unsigned integer
        for i in xrange(0, len(s), 8): 
            by = int(s[i:i+8], 2)
            bts.append(by)
        with open(filepath, 'w') as f:
            f.write(pack('{}B'.format(len(bts)),*bts))
            
    return encbin, add1, s, add2
    
  
def hf2bin256(encoding):
    '''Convert Huffman encoding to a binary string. That is, given encoding is 
    the mapping of symbols (integers) into code words.
    
    Does not work if there is more than 256 values to encode.
    
    Has some expectations of the encoding. Look the code.
    ''' 
    l = len(encoding.keys())
    lb = int(np.ceil(np.log2(max([len(e) for e in encoding.values()]))))
    s = "{:08b}".format(l)
    #m = np.ceil(np.log2(np.max([len(v) for v in encoding.values()])))
    #print lb
    items = encoding.items()
    #print items
    for k,v in items:
        #if k < 0 or k > 255:
        #    raise ValueError("k == {}".format(k))
        s += "{:08b}".format(k) # First encode the symbol into one byte
        s += ("{:0" + str(lb) + "b}").format(len(v)-1)
    
    for k,v in items:
        s += v
       
    #print len(s), len(s) % 8, len(s) / 8.0, h, 190*2*8
    add = len(s) % 8
    if add != 0:
        add = 8 - add
        for i in xrange(add):
            s += "0"
           
    return s, add
            
def bin2562hf(binstring,add):
    l = int(binstring[:8],2)
    b = binstring[8:-add]
    chars = []
    lengths = []
    encs = []
    for i in xrange(l):
        chars.append(int(b[:8],2))
        b=b[8:]
        lengths.append(int(b[:8],2))
        b=b[8:]
    for i in xrange(l):
        encs.append(b[:lengths[i]])
        b = b[lengths[i]:]
    return chars,encs
        
    
    
def _encode2dict(enc):
    d ={}
    for e in enc:
        d[e[0]] = e[1]
    return d

    
def encode(symb2freq):
    """Huffman encode the given dict mapping symbols to weights"""
    heap = [[wt, [sym, ""]] for sym, wt in symb2freq.items()]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))
    
 # The following added for caravan.dat:

def readCol(rowData, col, sep = ','):
    ''' Reads the specified column from multicolumn string data and returns it as a list.
      col = 'index of the desired column', sep = 'separator'. '''

    return [rowData[l].split(sep)[col] for l in range(len(rowData))]
    

def writeList(rowData, fileName):
    ''' Concatenates the elements of a string list as a single string and writes it on the hard drive. '''
    
    outList = ''
    for d in range(len(rowData)):
        outList = outList + str(rowData[d])
        if (d < len(rowData) - 1):
            outList = outList + '\n'
    fil = open(fileName, 'w')
    fil.write(outList)
    
def parseString(rowData, sep = '\n'):
    ''' Concatenates the elements of a list as a single string and returns it. '''
    outList = ''
    for d in range(len(rowData)):
        outList = outList + str(rowData[d])
        if (d < len(rowData) - 1):
            outList = outList + sep
    return outList
    
def codeCols(rowData, cols, sep = ','):
    ''' Constructs a Huffman coding for the given columns of a multicolumn data.
    Variable cols contains a list of the desired columns. Returns the encoded columns as
    a list of binary strings and a list containg all the corresponding encodings. '''
    
    bitit = [0 for d in range(len(cols))]
    koodit = [0 for d in range(len(cols))]

    for d in range(len(cols)):
        bitit[d], koodit[d] = digits2encode(readCol(rowData, cols[d]), unsign = True)
        
    return bitit, koodit
    
def chooseCols(rowData, cols, sep = ','):
    ''' Returns a list of strings that represent only a subset
    of the columns that the original rowData does. Variable cols
    contains a list of the desired columns. '''
    
    newRows = ['' for d in range(len(rowData))]
    newCols = ['' for d in range(len(cols))]
    
    for d in range(len(cols)):
        newCols[d] = readCol(rowData, cols[d], sep)

    for l in range(len(rowData)):
        #cols = [0 for k in range(len(cols))]
        
        for d in range(len(cols)):
            newRows[l] = newRows[l] + newCols[d][l]
            if (d < len(cols) - 1):
                newRows[l] = newRows[l] + ','
    
    return newRows

def mergeCols(colData1, colData2, cols1, sep = ','):
    ''' Merge two lists of column data into one.
    The list cols1 has to be ordered, otherwise this will not work. '''
    
    rowLength = len(colData1[0].split(sep)) + len(colData2[0].split(sep))
    newCols = ['' for t in range(len(colData1))]
    for t in range(len(newCols)):
        index = 0
        col1 = colData1[t].split(sep)
        col2 = colData2[t].split(sep)
        
        for n in range(rowLength):
            if (n == cols1[index]):
                newCols[t] = newCols[t] + col1[index]
                index += 1
            else:
                newCols[t] = newCols[t] + col2[n - index]
            if (n < rowLength - 1):
                newCols[t] = newCols[t] + ','
    return newCols 
    
def entropyCols(rowData, sep = ','):
    rowLength = len(rowData[0].split(sep))
    ent = [0 for d in range(rowLength)]
    
    for d in range(rowLength):
        en = 0
        col = [int(l) for l in readCol(rowData, d, sep)]
        laskuri = Counter(col)
        freq = [laskuri.values()[t] for t in range(len(laskuri))]
        
        for l in range(len(freq)):
            en = en + (freq[l] * (math.log(len(rowData), 2) - math.log(freq[l], 2)))
            
        ent[d] = "{0:.06f}".format((1.0 * en) / len(rowData))
    
    return ent
    
def entCol(rowData, col, sep = ','):
    
    en = 0
    col = [int(l) for l in readCol(rowData, col, sep)]
    laskuri = Counter(col)
    freq = [laskuri.values()[d] for d in range(len(laskuri))]
        
    for l in range(len(freq)):
        en = en + (freq[l] * (math.log(len(rowData), 2) - math.log(freq[l], 2)))
    
    return (1.0 * en) / len(rowData)

def jointEntCols(rowData, cols, sep = ','):
    ''' Gives the joint entropy of two columns '''
    
    en = 0
    col = [[] for d in range(len(cols))]
    comb = ['' for t in range(len(rowData))]
    
    for d in range(len(cols)):
        col[d] = [l for l in readCol(rowData, cols[d], sep)]
        
    for t in range(len(rowData)):
        for d in range(len(cols)):
            comb[t] = comb[t] + col[d][t]
            
    laskuri = Counter(comb)
    freq = [laskuri.values()[d] for d in range(len(laskuri))]
        
    for l in range(len(freq)):
        en = en + (freq[l] * (math.log(len(rowData), 2) - math.log(freq[l], 2)))
            
    return (1.0 * en) / len(rowData)
    
def mutualInfo(rowData, cols, sep = ','):
    ent = [entCol(rowData, cols[t], sep) for t in range(2)]
    joint = jointEntCols(rowData, cols, sep)
    return ent[0] + ent[1] - joint
    
def mutualInfo2(rowData, cols, ents, sep = ','):
    ''' Calculates the mutual information. The individual entropies are given in the variable ents. '''
    
    joint = jointEntCols(rowData, cols, sep)
    return ents[0] + ents[1] - joint
    
def mutualInfoNorm(rowData, cols, ents, sep = ','):
    joint = jointEntCols(rowData, cols, sep)
    m = max(ents[0], ents[1])
    if (m == 0):
        return 0
    return (ents[0] + ents[1] - joint) / m


def getHist(rowData, col, sep = ','):
    co = [int(r) for r in readCol(f, col)]
    num_bins = len(Counter(co))
    n, bins, patches = plt.hist(co, num_bins, normed=0, facecolor='green', alpha=0.5)
    plt.xlabel('Value')
    plt.ylabel('Freq')
    plt.title(r'Histogram of values in column #' + ' ' + str(col) + ':' )
    plt.show()
    
def writeBinary(binary, fileName):
    if len(binary) % 8 != 8 and len(binary) % 8 != 0:    # Fixing the length to be divisible by 8
    
        for x in xrange(8 - (len(binary) % 8)):
            binary += '0'

    bts = []
    for i in xrange(0, len(binary), 8):
        bit = binary[i:i+8]    
        by = int(bit, 2)  
        bts.append(by)

    fil = open(fileName, 'w')
    fil.write(pack('{}B'.format(len(bts)),*bts)) 
    
def charEncodeCols(rowData, sep = ','):
    rowLength = len(rowData[0].split(sep))
    newCols = ['' for t in range(len(rowData))]
    for t in range(len(rowData)):
        row = [int(d) for d in rowData[t].split(sep)]
        for d in range(rowLength):
            newCols[t] = newCols[t] + str(unichr(65 + row[d]))
    return newCols

def charUncodeCols(rowData, sep = ','):
    rowLength = len(rowData[0])
    newCols = ['' for t in range(len(rowData))]
    for t in range(len(rowData)):
        # row = [int(d) for d in rowData[t].split(sep)]
        for d in range(rowLength):
            newCols[t] = newCols[t] + str(ord(rowData[t][d]) - 65)
            if (d < rowLength - 1):
                newCols[t] = newCols[t] + sep
    return newCols


def writeZip(data, fileName):
    output = bz2.BZ2File(fileName + '.bz2', 'wb')
    try:
        output.write(data)
    finally:
        output.close()
    
def openZip(fileName):
    input_file = bz2.BZ2File(fileName + '.bz2', 'rb')
    try:
        a = input_file.read()
    finally:
        input_file.close()
    return a
    
def openCaravan(fileName, n, zipped = True):
    input_file = bz2.BZ2File(fileName + '.bz2', 'rb')
    try:
        a = input_file.read()
    finally:
        input_file.close()
    
    lengths = [0 for t in range(n)]
    parts = ['' for t in range(n)]
    
    temp = a[:200].split('_')
    temp = [int(d) for d in temp[:n]]
    index = 0
    
    for t in range(n):   # calculating the lengths of the parts
        lengths[t] = temp[t]
        index += len(str(temp[t])) + 1
    
    for t in range(n):   # reading in the parts
        if zipped:
            parts[t] = bz2.decompress(a[index : index + lengths[t]])
        else:
            parts[t] = a[index : index + lengths[t]]
        index += lengths[t]

    return parts