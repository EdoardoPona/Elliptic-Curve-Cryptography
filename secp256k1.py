import models
import builtins


def print(*args, **kwargs):
    """ custom print function, adding functionality for Points """
    new_args = []
    for arg in args:
        if builtins.isinstance(arg, models.Point):
            new_args.append("({0}, {1})".format(arg.x, arg.y))
        else:
            new_args.append(arg)

    builtins.print(*new_args, **kwargs)


p = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1
curve = models.Curve(a=0, b=7, p=p)

G_x = int("79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798", 16)
G_y = int("483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8", 16)

G = models.Point(G_x, G_y, curve)

priv_key0 = 17          # should pick a huge number for priv_key
pub_key0 = G*priv_key0

priv_key1 = 23
pub_key1 = G*priv_key1

print(pub_key0, pub_key1)
print(pub_key0*priv_key1 == pub_key1*priv_key0)         # should print True
