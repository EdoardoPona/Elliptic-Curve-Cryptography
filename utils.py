""" Helper functions
source: https://andrea.corbellini.name/2015/05/23/elliptic-curve-cryptography-finite-fields-and-discrete-logarithms/ """

import math



def truncate(number, digits=4) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


def standard_euclidean(a, b):
    """ returns GCD(a, b) """
    c, d = max((a, b)), min((a, b))
    r = c % d
    if r == 0:
        return d
    else:
        return standard_euclidean(d, r)


def extended_euclidean(a, b):
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = b, a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def inverse_of(n, p):
    """ returns multiplicative inverse of n modulo p """
    gcd, x, y = extended_euclidean(n, p)
    assert (n*x + p*y) % p == gcd

    if gcd != 1:
        raise ValueError('{} has no multiplicative inverse modulo {}'.format(n, p))
    else:
        return x % p
