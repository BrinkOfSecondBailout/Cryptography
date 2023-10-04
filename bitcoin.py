class FieldElement:
    def __init__(self, num, prime):
        # check if the number is within the range of the finite field
        if num >= prime or num < 0:
            error = 'Num {} not in field range 0 to {}'.format(num, prime - 1)
            raise ValueError(error)
        self.num = num
        self.prime = prime

    def __repr__(self):
        return 'FieldElement_{}({})'.format(self.prime, self.num)

    # overloads the == operator and check if the two elements are equal in terms of num and prime
    def __eq__(self, other):
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime

    def __ne__(self, other):
        return not (self == other)

    def __add__(self, other):
        # check if the primes are the same, if not then it's in two different fields
        if self.prime != other.prime:
            raise TypeError('Cannot add two numbers in different Fields')
        # add the two numbers modularly
        num = (self.num + other.num) % self.prime
        return self.__class__(num, self.prime)

    def __sub__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot subtract two numbers in different Fields')
        # subtract the two numbers modularly
        num = (self.num - other.num) % self.prime
        return self.__class__(num, self.prime)

    def __mul__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot multiply two numbers in different Fields')
        # multiply the two numbers modularly
        num = (self.num * other.num) % self.prime
        return self.__class__(num, self.prime)

    def __pow__(self, exponent):
        # n calculates the exponent after applying the modulo operation with self.prime - 1, which is the order of the field
        n = exponent % (self.prime - 1)
        # calculates the result of raising num to the exponent, n
        num = pow(self.num, n, self.prime)
        return self.__class__(num, self.prime)

    def __truediv__(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot divide two numbers in different Fields')
        num = (self.num * pow(other.num, self.prime - 2, self.prime)) % self.prime
        return self.__class__(num, self.prime)


class Point:
    def __init__(self, x, y, a, b):
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        # check if both x and y are None, this indicates the point is at infinity, return without further checks
        if self.x is None and self.y is None:
            return
        if self.y**2 != self.x**3 + a * x + b:
            raise ValueError('({}, {}) is not on the curve'.format(x, y))

    def __repr__(self):
        if self.x is None:
            return 'Point(infinity)'
        elif isinstance(self.x, FieldElement):
            return 'Point({},{})_{}_{} FieldElement({})'.format(
                self.x.num, self.y.num, self.a.num, self.b.num, self.x.prime)
        else:
            return 'Point({},{})_{}_{}'.format(self.x, self.y, self.a, self.b)

    def __add__(self, other):
        # check if the two points are on the same elliptic curve
        if (self.a != other.a or self.b != other.b):
            raise TypeError(
                'Points {}, {} are not on the same curve'.format(self, other))
        # check if either point is infinity, if it is, return the other point
        if self.x is None:
            return other
        if other.x is None:
            return self
        # check if the x coordinates of self and other are different, this indicates they are not the same and are not inverses of each other, add using the elliptic curve addition formula:
        if self.x != other.x:
            s = (other.y - self.y) / (other.x - self.x)
            x = s**2 - self.x - other.x
            y = s * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)
        # check if the two points are the same, then we use the elliptic curve doubling formula:
        if self == other:
            s = (3 * self.x**2 + self.a) / (2 * self.y)
            x = s**2 - 2 * self.x
            y = s * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)
        # check if the two points have the same x coordinate y have a coordinate of 0, this indicates it is a additive identity element, return the point at infinity
        if self.x == other and self.y == 0 * self.x:
            return self.__class__(None, None, self.a, self.b)
        # check if the two points have the same x coordinate but different y, this indicates they are inverses of each other, return the point at infinity
        if self.x == other.x and self.y != other.y:
            return __class__(None, None, self.a, self.b)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.a == other.a and self.b == other.b

    def __ne__(self, other):
        return not (self == other)


# def on_curve(x, y):
#     return y**2 == x**3 + a*x + b


prime = 223
a = FieldElement(0, prime)
b = FieldElement(7, prime)
x1 = FieldElement(170, prime)
y1 = FieldElement(142, prime)
x2 = FieldElement(60, prime)
y2 = FieldElement(139, prime)

p1 = Point(x1, y1, a, b)
p2 = Point(x2, y2, a, b)
p3 = p1 + p2
print(p3)
