'''Various utility functions
'''
from collections import Counter
from heapq import heappush, heappop, heapify

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