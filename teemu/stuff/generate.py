import numpy as n
r=open("d","r").read().split("\n")
r.pop()
r = [int(x) for x in r]
def f(x):
	return n.round(n.array([min((1698-10.79*i)*(n.abs(n.cos((i+1)/6))-1)+484,34) for i in x]))
y=f(n.linspace(0,99,num=100))
v=y+r
n.savetxt("curve1.dat",v,"%d")
