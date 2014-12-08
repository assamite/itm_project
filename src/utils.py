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