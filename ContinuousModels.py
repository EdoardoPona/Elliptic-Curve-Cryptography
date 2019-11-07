import builtins
import utils


def print(*args, **kwargs):
    """ custom print function, adding functionality for Points """
    new_args = []
    for arg in args:
        if builtins.isinstance(arg, Point):
            new_args.append("({0}, {1})".format(arg.x, arg.y))
        else:
            new_args.append(arg)

    builtins.print(*new_args, **kwargs)


class Curve:

    def __init__(self, a, b):
        """ defines an elliptic curve of with the form: y**2 = x**3 + ax + b """
        assert (4*a**3 + 27*b**2 != 0)          # excluding singular curves
        self.a, self.b = a, b
        self.identity = Point(None, None, self, is_identity=True)

    def __eq__(self, other):
        """ overloading curve equality comparison, simply checking for the coefficients """
        return self.a == other.a and self.b == other.b

    def belongs_to_curve(self, x, y):
        """ does point belong to this curve """
        return utils.truncate(y**2) == utils.truncate(x**3 + self.a*x + self.b)

    def get_slope(self, point):
        x, y = point.x, point.y
        return (3*x**2 + self.a) / (2*y)


class Point:

    def __init__(self, x, y, curve, is_identity=False):

        if not is_identity:
            assert (curve.belongs_to_curve(x, y))

        self.x, self.y = x, y
        self.curve = curve
        self.is_identity = is_identity

    def __eq__(self, other):
        """ overloading equality comparison """
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y and self.curve == other.curve
        else:
            return False

    def __add__(self, Q):
        """ overloading addition with group operation  """

        # checking for edge cases
        if self.is_identity:
            return Q
        elif Q.is_identity:
            return self
        elif self == -Q:          # adding to its inverse
            return self.curve.identity
        elif self == Q:         # doubling the point
            return self.double()

        x_p, y_p = self.x, self.y   # making things more readable

        m = (y_p - Q.y) / (x_p - Q.x)
        x_r = m**2 - x_p - Q.x
        y_r = y_p + m*(x_r - x_p)

        return Point(x_r, -y_r, self.curve)

    def __sub__(self, other):
        return self + (-other)

    def __neg__(self):
        """ overloading unary minus with point inverse """
        if self.is_identity:
            return self
        return Point(self.x, -self.y, self.curve)

    def __mul__(self, n):
        binary = reversed(bin(n)[2:])           # [2:] removes the prefix
        S = self.curve.identity
        addend = self

        for i in binary:
            if i == '1':
                S = S + addend
            addend = addend.double()
        return -S

    def double(self):
        if self.is_identity:
            return self

        m = self.curve.get_slope(self)
        x_r = m**2 - 2*self.x
        y_r = self.y + m*(x_r - self.x)
        return Point(x_r, -y_r, self.curve)

