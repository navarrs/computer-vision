import numpy as np
from util import *
# do not include any more libraries here!
# do not put any code outside of functions!

############################## Q 2.1 ##############################
# initialize b to 0 vector
# b should be a 1D array, not a 2D array with a singleton dimension
# we will do XW + b. 
# X be [Examples, Dimensions]
def initialize_weights(in_size, out_size, params, name=''):
    ##########################
    ##### your code here #####
    ##########################
    xavier = np.sqrt(6) / np.sqrt(in_size + out_size)
    W = np.random.uniform(low=-xavier, high=xavier, size=(in_size, out_size))
    b = np.zeros(shape=(out_size), dtype=np.float32)

    params['W' + name] = W
    params['b' + name] = b

############################## Q 2.2.1 ##############################
# x is a matrix
# a sigmoid activation function
def sigmoid(x):
    ##########################
    ##### your code here #####
    ########################## 
    res = 1.0 / (1.0 + np.exp(-x))
    return res

############################## Q 2.2.1 ##############################
def forward(X, params, name='', activation=sigmoid):
    """
    Do a forward pass

    Keyword arguments:
    X -- input vector [Examples x D]
    params -- a dictionary containing parameters
    name -- name of the layer
    activation -- the activation function (default is sigmoid)
    """
    # get the layer parameters
    W = params['W' + name]
    b = params['b' + name]

    ##########################
    ##### your code here #####
    ##########################
    pre_act = X @ W + b
    post_act = activation(pre_act)

    # store the pre-activation and post-activation values
    # these will be important in backprop
    params['cache_' + name] = (X, pre_act, post_act)
    return post_act

############################## Q 2.2.2  ##############################
# x is [examples,classes]
# softmax should be done for each row
def softmax(x):
    
    ##########################
    ##### your code here #####
    ##########################
    res = np.zeros(shape=x.shape)
    for r in range(x.shape[0]):
        c = -np.max(x[r])
        s = np.exp(x[r] + c)
        S = np.sum(s)
        res[r] = s / S
                
    return res

############################## Q 2.2.3 ##############################
# compute total loss and accuracy
# y is size [examples,classes]
# probs is size [examples,classes]
def compute_loss_and_acc(y, probs):

    ##########################
    ##### your code here #####
    ##########################
    N = len(y)
    acc = 0.0
    loss = -np.sum(y * np.log(probs))
    y_labels = np.argmax(y, axis=1)
    y_hat_labels = np.argmax(probs, axis=1)
    acc = len(np.where(y_labels == y_hat_labels)[0]) / N
    return loss, acc 

############################## Q 2.3 ##############################
# we give this to you
# because you proved it
# it's a function of post_act
def sigmoid_deriv(post_act):
    res = post_act*(1.0-post_act)
    return res

def backwards(delta, params, name='', activation_deriv=sigmoid_deriv):
    """
    Do a backwards pass

    Keyword arguments:
    delta -- errors to backprop
    params -- a dictionary containing parameters
    name -- name of the layer
    activation_deriv -- the derivative of the activation_func
    """
    # everything you may need for this layer
    W = params['W' + name]
    b = params['b' + name]
    X, pre_act, post_act = params['cache_' + name]

    # do the derivative through activation first
    # then compute the derivative W,b, and X
    ##########################
    ##### your code here #####
    ##########################
    delta *= activation_deriv(post_act)
    grad_W = (delta.T @ X).T
    grad_X = delta @ W.T
    grad_b = delta.T @ np.ones(delta.shape[0])
    # print(grad_W.shape, W.shape)
    # print(grad_X.shape, X.shape)
    # print(grad_b.shape, b.shape)

    # store the gradients
    params['grad_W' + name] = grad_W
    params['grad_b' + name] = grad_b
    return grad_X

############################## Q 2.4 ##############################
# split x and y into random batches
# return a list of [(batch1_x,batch1_y)...]
def get_random_batches(x, y, batch_size):
    batches = []
    ##########################
    ##### your code here #####
    ##########################
    rng_state = np.random.get_state()
    np.random.shuffle(x)
    np.random.set_state(rng_state)
    np.random.shuffle(y)
    
    n_batches = int(len(x)/batch_size)
    for n in range(n_batches):
        s = n * batch_size
        # print(f"start{s} end{s+batch_size}")
        batches.append((x[s:s+batch_size], y[s:s+batch_size]))
    
    return batches
