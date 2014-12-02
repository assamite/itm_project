'''Caravan.dat thingies
'''
import numpy as np
from matplotlib import pyplot as plt
from collections import Counter
import operator

def read_data(filepath = "../data/caravan.dat"):
    '''Read caravan.dat'''
    data = open(filepath).read().split("\n")[:-1] # remove empty line in the end
    data = [d.split() for d in data]
    for i,l in enumerate(data):
        data[i] = [int(d.strip()) for d in l]
        
    data = np.array(data)
    print data.shape
    return data


def mutual_info(data, plot = True):
    '''Calculate mutual information of columns.'''
    cols = data.shape[1] 
    rows = data.shape[0]
    dists = np.eye(cols)
    
    counters = []
    for c in xrange(cols):
        counters.append(Counter(data[:, c]))
    
    for c1 in xrange(cols):
        col1 = data[:,c1]
        u1 = sorted(np.unique(col1))
        for c2 in xrange(cols):
            if c1 == c2: continue
            col2 = data[:, c2]
            u2 = sorted(np.unique(col2))
            col_dict = dict.fromkeys(u1, {})
            for k, v in col_dict.items():
                col_dict[k] = dict.fromkeys(u2, 0.0)
            for i in xrange(rows):
                n1 = col1[i]
                n2 = col2[i]
                col_dict[n1][n2] += 1
            mi = 0.0
            for k1, v1 in col_dict.items():
                pk1 = float(counters[c1][k1]) / rows
                for k2, v2 in v1.items():
                    pk1k2 = float(v2) / rows
                    pk2 = float(counters[c2][k2]) / rows
                    if pk1k2 > 0.0:
                        mi += pk1k2 * np.log2(pk1k2 / (pk1 * pk2))
            print c1, c2, mi
            dists[c1][c2] = mi
    
    if plot:
        heatmap(dists, title = "Caravan Column Mutual Information")
            
    return dists


def pairwise_dependencies(data, normalize = False, plot = True):
    '''Calculate pairwise "dependencies" for columsn.'''
    cols = data.shape[1] 
    rows = data.shape[0]
    dists = np.eye(cols)
    
    counters = []
    for c in xrange(cols):
        counters.append(Counter(data[:, c]))
    
    for c1 in xrange(cols):
        col1 = data[:,c1]
        u1 = sorted(np.unique(col1))

        for c2 in xrange(cols):
            if c1 == c2: continue
            col2 = data[:, c2]
            u2 = sorted(np.unique(col2))
            col_dict = dict.fromkeys(u1, {})
            for k, v in col_dict.items():
                col_dict[k] = dict.fromkeys(u2, 0.0)
            for i in xrange(rows):
                n1 = col1[i]
                n2 = col2[i]
                col_dict[n1][n2] += 1
            dv = 0.0
            for k1, v1 in col_dict.items():
                sv = sum(v1.values())
                mv = max(v1.values())
                cv = float(mv) / sv
                if normalize:
                    cv = cv * float(counters[c1][k1]) / rows
                dv += cv
            if not normalize: 
                dv = dv / len(col_dict.keys())        
            print c1, c2, dv
            dists[c1][c2] = dv
            
    if plot:
        heatmap(dists, title = "Caravan Column Pairwise 'Dependencies'")
            
    return dists
    

def heatmap(dists, title = "", size = 15, labels = None, filepath = None):
    '''Plot pairwise distance/similarity data as heat map.
    '''
    cols = dists.shape[0]
    
    fig, ax = plt.subplots()
    fig.set_size_inches(size, size)
    
    heatmap = ax.pcolor(dists, cmap=plt.cm.Blues)
    
    # put the major ticks at the middle of each cell
    ax.set_xticks(np.arange(dists.shape[0])+0.5, minor=False)
    ax.set_yticks(np.arange(dists.shape[1])+0.5, minor=False)
    cbar = plt.colorbar(heatmap)
    
    # want a more natural, table-like display
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    figure_title = title
    
    plt.text(0.5, 1.08, figure_title,
         horizontalalignment='center',
         fontsize=20,
         transform = ax.transAxes)
    
    if labels is not None:
        if not hasattr(labels, '__iter__'):
            labels = [str(d) for d in xrange(cols)]
        ax.set_xticklabels(labels, minor=False, rotation = 90)
        ax.set_yticklabels(labels, minor=False)
    
    if filepath:
        plt.savefig(filepath)
    
    plt.show()
    
    
def split_data(data, sdat_file = "../sdata/caravan.sdat"):
    sdata = [int(c) for c in open(sdat_file).read().split()]

    d0 = []
    d1 = []
    for i in xrange(data.shape[0]):
        if sdata[i] == 0:
            d0.append(data[i])
        else:
            d1.append(data[i])
    d0 = np.array(d0)
    d1 = np.array(d1)
    return d0, d1, sdata



            
                
if __name__ == "__main__":
    data = read_data()
    d0, d1, sdata = split_data(data)
    #dists = pairwise_dependencies(d0, normalize = False, plot = True)
    #dists = pairwise_dependencies(d1, normalize = False, plot = True)
    dists = mutual_info(d0, plot = True)
    dists = mutual_info(d1, plot = True)