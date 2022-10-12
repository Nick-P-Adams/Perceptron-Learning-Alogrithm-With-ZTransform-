# Implementation of the perceptron learning algorithm. Support the pocket version for linearly unseparatable data. 
# Authro: Bojian Xu, bojianxu@ewu.edu

#Important observation: 
#    - The PLA can increase or decrease $w[0]$ by 1 per update, so if there is a big difference between $w^*[0]$ and the #initial value of $w[0]$, the PLA is likely to take a long time before it halts. However, the theoretical bound $O((L/d)^2)$ #step of course still holds, where $L = \max\{\lVert x\rVert\}$ and $d$ is the margine size.
#    - This can solved by always have feature values within [0,1], because by doing so, the $x_0=1$ becomes relatively #larger (or one can also say $x_0$ becomes fairly as important as other feathers), which makes the changes to $w[0]$ much #faster. This is partially why nueral network requires all feature value to be [0,1] --- the so-called data normalization #process!!!

# Another reason for normalizing the feature into [0,1] is: no matter which Z space the samples are tranformed to, the Z-space sample features will still be in the [0,1] range. 

import numpy as np

import sys
sys.path.append("..")

from utils import MyUtils

class PLA:
    def __init__(self):
        self.w = None
        self.degree = 1
        
    def fit(self, X, y, pocket = True, epochs = 100, degree = 1):
        ''' X: n x d matrix 
            y: n x 1 vector of {+1, -1}
            degree: the degree of the Z space
            return w
        '''
        
        self.degree = degree
        if(self.degree > 1):
            X = MyUtils.z_transform(X, degree = self.degree)
            
        n, d = X.shape
        X = np.insert(X, 0, 1, axis = 1) # add the column of x_0 = 1 features.
        self.w = np.array([[0],]* (d+1)) # init the w vector

        updated = True
                          
        if not pocket:
            while updated:
                updated = False
                for i in range(n):
                    if np.sign(X[i] @ self.w) != y[i,0]:
                        self.w = self.w + (y[i,0] * X[i]).reshape(-1,1)
                        updated = True
        else:
            errors = n # record the smallest number of errors so far
            best_w = self.w # record the best w vector so far
            while updated and epochs > 0:
                updated = False
                epochs -= 1
                for i in range(n):
                    if np.sign(X[i] @ self.w) != y[i,0]:
                        self.w = self.w + (y[i,0] * X[i]).reshape(-1,1)
                        updated = True
                        cur_errors = self._error_z(X, y)
                        if cur_errors < errors:
                            errors = cur_errors
                            best_w = self.w
            self.w = best_w
                          
        return self.w
    
    def predict(self, X):
        ''' x: n x d matrix 
            return: n x 1 vector, the labels of samples in X
        '''
        if(self.degree > 1):
            X = MyUtils.z_transform(X, degree = self.degree)

        X = np.insert(X, 0, 1, axis = 1) # add the x_0 = 1 feature

        return np.sign(X @ self.w)
    

    def _error_z(self, Z, y):
        ''' Used internally by the fit function to count the misclassied samples.
            The sample Z is in the Z space with the bias column.
            
            Z: n x (d'+1) matrix 
            y: n x 1 vector
            
            return: the number of misclassifed elements in Z using self.w
        '''
                    
        n = Z.shape[0]

        # this is better code than the loop below but needs a test when time is available        
        y_hat = Z @ self.w
        y_hat = np.sign(y_hat)
        errors = n - np.sum(y_hat == y)
                
        return errors


    def error(self, X, y):
        ''' X: n x d matrix 
            y: n x 1 vector
            return the number of misclassifed elements in X using self.w
        '''
        
        if(self.degree > 1):
            X = MyUtils.z_transform(X, degree = self.degree)
            
        X = np.insert(X, 0, 1, axis = 1) # add the column of x_0 = 1 features.

        # this is better code than the loop below but needs a test when time is available        
        y_hat = X @ self.w
        y_hat = np.sign(y_hat)
        errors = np.sum(y_hat != y)
                
        return errors


    