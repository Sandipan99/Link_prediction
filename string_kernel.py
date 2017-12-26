import numpy as np

def sigma(x):
    return 1/(1+exp(-x))

def StringKernelFeedForward(sequence,W,n): # Cell_state[0] initialized to 0s
    k = len(sequence[0])
    Cell_state = np.zeros((n+1,k), dtype=np.float)
    h = np.zeros((len(sequence),k), dtype=np.float)
    for t in xrange(len(sequence)):
        Cell_state[1] = l*Cell_state[0] + W[0]*sequence[t]
        for j in xrange(2,n+1):
            Cell_state[j] = l*Cell_state[j] + Cell_state[j-1]+(W[j-1]*sequence[t])

        h[t] = map(lambda x:sigma(x),Cell_state[n])   

        return h
