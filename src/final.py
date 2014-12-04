'''Playing with Final.dat
'''
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from matplotlib import cm
from scipy.optimize import curve_fit


def read_data(datapath = "../data/final.dat", sdatapath = "../sdata/final.sdat"):
    '''Read data and sdata for final.dat. Return numpy arrays X,Y,Z where X
    is the data ja Y,Z the side data.'''
    data = np.array([float(e) for e in open(datapath).read().split()])
    sdata = [e for e in open(sdatapath).read().split("\n")][:-1]
    Y = np.zeros(data.shape)
    Z = np.zeros(data.shape)
    for i,e in enumerate(sdata):
        y,z = e.split()
        Y[i] = float(y)
        Z[i] = float(z)
       
    return data, Y, Z



def model(D, p00, p10, p01, p20, p11, p02, p30, p21, p12, p03, p31, p22, p13, p04):
    Y, Z = D[:, 0], D[:, 1]
    return p00 + p10*Y + p01*Z + p20*Y**2 + p11*Y*Z + p02*Z**2 + p30*Y**3 +\
        p21*(Y**2)*Z + p12*Y*(Z**2) + p03*Z**3 + p31*(Y**3)*Z + p22*(Y**2)*(Z**2) +\
        p13*Y*(Z**3) + p04*Z**4


def get_grid(ymin, ymax, zmin, zmax):
    ny = 20
    nz = 20
    yy, zz = np.meshgrid(np.linspace(ymin, ymax, ny), 
                         np.linspace(zmin, zmax, nz))
    return yy, zz
  
  
def fit_surface():
    X,Y,Z = read_data()
    xmin, xmax = min(X)*1.05, max(X)*1.05
    ymin, ymax = min(Y)*1.05, max(Y)*1.05
    zmin, zmax = min(Z)*1.05, max(Z)*1.05
    data = np.array([Y,Z])
    data = np.transpose(data)
    fX, fY, fZ = X, Y, Z
    popt, popcov = curve_fit(model, data, X)
    #print popt
    yy, zz = get_grid(ymin, ymax, zmin, zmax)
    yzdata = np.transpose(np.array([yy.flatten(), zz.flatten()]))
    opt_params = [0.7662, -0.02181, 0.2393, 0.2502, -0.2056, 0.03911, 0.011, -0.02859, -0.007768, -0.1531, -0.04139, -0.2023, 0.1685, 0.1065]
    xx = model(yzdata, *opt_params)
    xx = xx.reshape(yy.shape)
    return xx, yy, zz


'''
    Optimal params from matlab.
       p00 =      0.7662  (0.3584, 1.174)
       p10 =    -0.02181  (-0.5342, 0.4906)
       p01 =      0.2393  (-0.2892, 0.7677)
       p20 =      0.2502  (-0.01344, 0.5139)
       p11 =     -0.2056  (-0.8177, 0.4065)
       p02 =     0.03911  (-0.6076, 0.6858)
       p30 =       0.011  (-0.1739, 0.1959)
       p21 =    -0.02859  (-0.2352, 0.1781)
       p12 =   -0.007768  (-0.2188, 0.2033)
       p03 =     -0.1531  (-0.3761, 0.07004)
       p31 =    -0.04139  (-0.2199, 0.1371)
       p22 =     -0.2023  (-0.3645, -0.0401)
       p13 =      0.1685  (-0.01294, 0.35)
       p04 =      0.1065  (-0.08225, 0.2952)
'''
   
def plot3D(S = None):
    '''Plot final.dat in 3D space. If specified, S must be an iterable
    of size 3 which specifies (the fitted) surface points to plot.
    '''    
    X,Y,Z = read_data()  
    fig = plt.figure() 
    ax = fig.add_subplot(111, projection='3d')  
    ax.scatter(X,Y,Z)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    if S is not None:
        SX, SY, SZ = S
        ax.plot_surface(SX,SY,SZ, color = (1, 0, 1, 0.3))
    
    plt.show()
    
    
    
    
if __name__ == "__main__":
    S = fit_surface()
    plot3D(S = S)
