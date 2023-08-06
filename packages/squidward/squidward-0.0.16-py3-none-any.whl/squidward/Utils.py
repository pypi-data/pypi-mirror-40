import sys
import warnings
import functools
import numpy as np
import scipy.linalg as la
from scipy.special import expit

np.seterr(over="raise")

def sigmoid(z, ingore_overflow=False):
    try:
        return 1.0 / (1.0 + np.exp(-z))
    except Exception as e:
        if "overflow encountered in exp" in str(e):
            if ingore_overflow:
                return 1.0 / (1.0 + expit(-z))
        raise e

def softmax(z):
    return z / z.sum(axis=1).reshape(-1, 1)

def is_invertible(arr, strength='condition'):
    if strength=='cramer':
        return np.linalg.det(arr) == 0.0
    if strength=='rank':
        return arr.shape[0] == arr.shape[1] and np.linalg.matrix_rank(arr) == arr.shape[0]
    return 1.0 / np.linalg.cond(arr) >= sys.float_info.epsilon

def check_valid_cov(cov):
    if not is_invertible(cov):
        warnings.warn('Cov has high condition. Inverting matrix may result in errors.')
    var = np.diag(cov)
    if var[var < 0].shape[0] != 0:
        raise Exception('Negative values in diagonal of covariance matrix.\nLikely cause is kernel inversion instability.\nCheck kernel variance.')
    return None

def atleast_2d(x):
    if len(x.shape) == 1:
        x = x.reshape(-1, 1)
    if len(x.shape) == 2 and x.shape[0] == 1:
        x = x.reshape(-1, 1)
    return x

def atmost_1d(x):
    if len(x.shape) == 1:
        return x
    elif len(x.shape) == 2:
        if x.shape[0] == 1:
            return x[0,:]
        elif x.shape[1] == 1:
            return x[:,0]
        else:
            raise Exception("Not appropriate input shape.")
    else:
        raise Exception("Not appropriate input shape.")

def make_grid(coordinates=(-10, 10, 1)):
    min_, max_, grain = coordinates
    if min_ >= max_:
        raise Exception("Min value greater than max value.")
    x_test = np.mgrid[min_:max_:grain, min_:max_:grain].reshape(2, -1).T
    if np.sqrt(x_test.shape[0]) % 2 == 0:
        size = int(np.sqrt(x_test.shape[0]))
    else:
        raise Exception('Plot topology not square!')
    return x_test, size

def invert(Arr, method='inv'):
    if not is_invertible(Arr):
        warnings.warn('Matrix has high condition. Inverting matrix may result in errors.')
    if method == 'inv':
        return np.linalg.inv(Arr)
    elif method == 'pinv':
        return np.linalg.pinv(Arr)
    elif method == 'solve':
        I = np.identity(Arr.shape[-1], dtype=Arr.dtype)
        return np.linalg.solve(Arr, I)
    elif method == 'cholesky':
        c = np.linalg.inv(np.linalg.cholesky(Arr))
        return np.dot(c.T, c)
    elif method == 'svd':
        u, s, v = np.linalg.svd(Arr)
        return np.dot(v.transpose(), np.dot(np.diag(s**-1), u.transpose()))
    elif method == 'lu':
        P, L, U = la.lu(Arr)
        invU = np.linalg.inv(U)
        invL = np.linalg.inv(L)
        invP = np.linalg.inv(P)
        return invU.dot(invL).dot(invP)
    raise Exception('Invalid inversion method argument.')

def onehot(a, num_classes=None, safe=True):
    """
    """
    if num_classes is None:
        num_classes = np.unique(a).shape[0]
    if safe:
        if num_classes != np.unique(a).shape[0]:
            raise Exception('Number of unique values does not match num_classes argument.')
    return np.squeeze(np.eye(num_classes)[a.reshape(-1)])

def reversehot(x):
    """
    """
    if len(x.shape) > 1:
        if len(x.shape) == 2:
            if x.shape[0] == 1:
                return x[0,:]
            if x.shape[1] == 1:
                return x[:,0]
        return x.argmax(axis=1)
    return x

def deprecated(func):
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.
    """
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        # https://stackoverflow.com/questions/2536307/decorators-in-the-python-standard-lib-deprecated-specifically
        # may not want to turn filter on and off
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning,
                      stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)
    return new_func
