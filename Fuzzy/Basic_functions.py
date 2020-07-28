from scipy import integrate
import matplotlib.pyplot as plt


def max_function(functions):
    def f(x):
        return (max([fct(x) for fct in functions]))
    
    return f


def min_function(functions):
    def f(x):
        return (min([fct(x) for fct in functions]))
    
    return f


def constant_function(c):
    def f(x):
        return c
    
    return f


def centroid(f):
    if integrate.quad(f, 0, 1)[0] == 0:
        return 0
    else:
        def integrand(x):
            return x * f(x)
        
        return (integrate.quad(integrand, 0, 1)[0]) / (integrate.quad(f, 0, 1)[0])


def val_max(f):
    return max([f(x / 100) for x in range(0, 101)])


def first_max(f):
    max = val_max(f)
    return [x / 100 for x in range(0, 101) if (f(x / 100) - max) < 0.01 * max][0]


def mean_max(f):
    max = val_max(f)
    L = [x / 100 for x in range(0, 101) if (f(x / 100) - max) < 0.01 * max]
    return sum(L) / len(L)
