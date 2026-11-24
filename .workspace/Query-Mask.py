import numpy as np

K = np.array([[1.0, 0.0][0.0, 1.0]])

V = np.array([[2.0, 0.0], [0.0, 3.0]])

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / np.sum(e_X)

def compute_attention(Q, K, V):
    d_k = K.shape[-1]

    socres = 
    return output

