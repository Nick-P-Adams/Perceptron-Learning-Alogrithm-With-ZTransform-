import numpy as np
import utils
import math

def combinations(r,d):
    sum = 0
    for i in range(r):
        sum += math.comb(i+d,d-1)
    return sum

def generateX(n,d):
    return np.arange(1,n*d + 1).reshape(n,d)

def getExpectedResults(file="output.npz"):
    container = np.load(file)
    data = [container[key] for key in container]
    return data

Z_list = []
n = 5
max_d = 4
max_r = 4
data = getExpectedResults()
for d in range(1,max_d+1):
    for r in range(1,max_r+1):
        X = generateX(n,d)
        Z = utils.MyUtils.z_transform(X,degree=r)
        cols = combinations(r,d)
        assert cols == Z.shape[1], f"An incorrect number of columns were generated for degree {r} and {d} feature(s).\nExpected: {cols}\nFound: {Z.shape[1]}"
        data_idx = max_d*(d-1) + (r-1)
        assert np.all(data[data_idx] == Z), f"Mismatched Z matrices for degree {r} and {d} feature(s).\nExpected:\n{data[data_idx]}\nFound:\n{Z}"
