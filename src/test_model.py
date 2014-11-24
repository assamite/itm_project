'''Test ty.txt model for best parameters up and down.
'''
import sys
import utils
import numpy as np
from collections import Counter
def model(n,y,addition,a,b,c,d,e,f,g,h,i,j,k,x):
    if(y<1250*x):
        return (-1*np.abs(a*n+b))*(np.abs(np.cos(c*n))-1)**2+d + addition
    else:
        return (e*(n-1250*x)+f)*(np.abs(np.cos(g*(n-1250*x)+h)+i)+j)+k + addition


def return_smaller(orig,n,y,plus,minus,*args):
    plus_d = model(n,y,plus,*args)
    minus_d = model(n,y,minus,*args)
    if np.abs(orig-plus_d) <= np.abs(orig-minus_d):
        return (plus_d, 1)
    else:
        return (minus_d, 0)
    
    
def get_hf_len(counter):
    enc = utils._encode2dict(utils.encode(counter))
    l = 0
    h = 0
    for k,v in counter.items():
        l+= len(enc[k])*v
        h+= len(enc[k])
        
    return (16*len(enc), h, l)
    

def test(filepath):
    '''Test 2-model scenario for ty.txt'''
    orig = np.array([float(i.strip()) for i in open(filepath).read().split()])
    ran = np.linspace(0,1999,num=10000)
    p = [-1.08589, 1365.49, 0.016679, 64.559187,1.131426,5601.76666,0.033079,-25.24067,-0.302556,-0.706202,57.668242,5]
    upper = range(0, 110)
    lower = range(0, 110)
    
    best = sys.maxint
    best_residuals = []
    best_models = []
    best_plus = 0
    best_minus = 0
    best_res = []
    for i in upper:
        plus = i
        for j in lower:
            minus = -j
            print "Trying plus={} minus={}".format(plus, minus)
            estimates = []
            models = []
            for y,n in enumerate(ran):
                diff, m = return_smaller(orig[y], n, y, plus, minus, *p)
                estimates.append(diff)
                models.append(m)
            estimates = np.array([round(e, 2) for e in estimates])
            residuals = orig - estimates 
            signs = reduce(lambda x,y: x+('0' if y<=0 else '1'), residuals, "")
            residuals_abs = [np.abs(r) for r in residuals]
            residuals_int = [int(r) for r in residuals_abs]
            residuals_dec = np.array([str(round(r - int(r),2)).split(".")[1] for r in residuals_abs])
            residuals_dec = np.array([r +"0" if len(r)==1 else r for r in residuals_dec])
            residuals_dec_int = [int(r) for r in residuals_dec]
            res = residuals_int + residuals_dec_int
            res_set = set(res)
            s,e,l = get_hf_len(Counter(res))
            if s+e+l < best:
                best_res = res
                best_residuals = residuals
                best_models = models
                best_plus = plus
                best_minus = minus
                best = s+e+l
                s,e,l = get_hf_len(Counter(res))
                print Counter(res)
                print "Got shorter approx. Huffman code length: {}+{}+{}={} / 8 = {}".format(s,e,l,s+e+l, (s+e+l) / 8)
                print "Residual set size: ", len(res_set)
       
    print            
    print "***********************************"
    print "Best models: plus = {}, minus = {}".format(best_plus, best_minus)
    s,e,l = get_hf_len(Counter(best_res))
    print "Best Huffman code length approx: {}+{}+{}={} / 8 = {}".format(s,e,l,s+e+l, (s+e+l) / 8)
    print "Residual set length: {}".format(len(set(best_res)))
                
                

def test2(filepath):   
    '''Test one model scenario for ty.txt.'''             
    orig = np.array([float(i.strip()) for i in open(filepath).read().split()])
    ran = np.linspace(0,1999,num=10000)
    p = [-1.08589, 1365.49, 0.016679, 64.559187,1.131426,5601.76666,0.033079,-25.24067,-0.302556,-0.706202,57.668242,5]
    cand = range(-110, 110)
    
    best = sys.maxint
    best_residuals = []
    best_cand = cand[0]
    best_res = []
    for i in cand:
        cand = i
        print "Trying model = {}".format(cand)
        estimates = []
        for y,n in enumerate(ran):
            diff = model(n, y, cand, *p)
            estimates.append(diff)
        estimates = np.array([round(e, 2) for e in estimates])
        residuals = orig - estimates 
        signs = reduce(lambda x,y: x+('0' if y<=0 else '1'), residuals, "")
        residuals_abs = [np.abs(r) for r in residuals]
        residuals_int = [int(r) for r in residuals_abs]
        residuals_dec = np.array([str(round(r - int(r),2)).split(".")[1] for r in residuals_abs])
        residuals_dec = np.array([r +"0" if len(r)==1 else r for r in residuals_dec])
        residuals_dec_int = [int(r) for r in residuals_dec]
        res = residuals_int + residuals_dec_int
        res_set = set(res)
        s,e,l = get_hf_len(Counter(res))
        if s+e+l < best:
            best_res = res
            best_residuals = residuals
            best_cand = cand
            best = s+e+l
            s,e,l = get_hf_len(Counter(res))
            print Counter(res)
            print "Got shorter approx. Huffman code length: {}+{}+{}={} / 8 = {}".format(s,e,l,s+e+l, (s+e+l) / 8)
            print "Residual set size: ", len(res_set)
        print
       
    print            
    print "***********************************"
    print "Best model: {}".format(best_cand)
    s,e,l = get_hf_len(Counter(best_res))
    print "Best Huffman code length approx: {}+{}+{}={} / 8 = {}".format(s,e,l,s+e+l, (s+e+l) / 8)
    print "Residual set length: {}".format(len(set(best_res)))




if __name__ == "__main__":
    test2("../data/ty.txt")