import math
class Vec3:
    @staticmethod
    def null():
        return Vec3(0,0,0)
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z
    def length(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
    def __str__(self):
        return '({};{};{})'.format(self.x, self.y, self.z)
    def __sub__(self, oth):
        return Vec3(self.x - oth.x, self.y - oth.y, self.z - oth.z)
    def __add__(self, oth):
        return Vec3(self.x + oth.x, self.y + oth.y, self.z + oth.z)
    def __eq__(self, oth):
        return self.x == oth.x and self.y == oth.y and self.z == oth.z
    def __mul__(self, oth):
        if type(oth) == Vec3:
            return scalar(self, oth)
        else:
            return Vec3(self.x * oth, self.y * oth, self.z * oth)
    def __truediv__(self, oth):
        return Vec3(self.x / oth, self.y / oth, self.z / oth)
    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)
    def __pos__(self):
        return self
    def __ne__(self, oth):
        return not self == oth
    def normalize(self):
        return self / self.length()

def cross_match(source, target, hit):
    if (hit - source).length() <= 0.1 ** 3:
        return False
    return ((target - source).normalize() + (hit - source).normalize()).length() >= 1

def light_ok(source, target, cross):
    return (cross - source).length() >= (target - source).length() - 0.1 ** 2

def scalar(a:Vec3, b:Vec3):
    return a.x * b.x + a.y * b.y + a.z * b.z
def cos(a:Vec3, b:Vec3):
    return (a * b) / (a.length() * b.length())
def oblique(a:Vec3, b:Vec3):
    return Vec3(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x)

def do_sq_equation(k1, k2, k3):
    if k2 ** 2 - 4 * k1 * k3 < 0:
        return (None, None)

    dscr = (k2 ** 2 - 4 * k1 * k3) ** 0.5

    return ((-k2 - dscr) / (2 * k1), (-k2 + dscr) / (2 * k1))
if __name__ == '__main__':
    a, b, c = map(int, input().split())
    print(do_sq_equation(a, b, c))
