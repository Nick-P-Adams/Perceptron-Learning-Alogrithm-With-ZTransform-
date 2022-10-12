##### >>>>>> Nick Adams 00883496


# Various tools for data manipulation. 



import numpy as np
import math

class MyUtils:
    
    def z_transform(X, degree = 2):
        ''' Transforming traing samples to the Z space
            X: n x d matrix of samples, excluding the x_0 = 1 feature
            degree: the degree of the Z space
            return: the n x d' matrix of samples in the Z space, excluding the z_0 = 1 feature.
            It can be mathematically calculated: d' = \sum_{k=1}^{degree} (k+d-1) \choose (d-1)
        '''
        
        if degree <= 1:
            return X
        
        _, d = X.shape
        Z = X.copy()
        B = []
        
        for i in range(degree):
            B.append(math.comb(d + i, d - 1))
               
        l = np.linspace(0, np.sum(B) - 1, num=np.sum(B), dtype=int)
        
        q = 0 # the total size of all buckets before the previous bucket
        p = d # the size of the previous bucket
        
        for i in range(1, degree):
            g = p
            
            for j in range(q, p):
                head = l[j]
                
                for k in range(head, d):
                    temp = (Z[:, j] * X[:, k]).reshape(-1, 1)
                    Z = np.append(Z, temp, axis=1)
                    l[g] = k
                    g += 1
                    
            q = p
            p += B[i]
            
        return Z
    
    
    