#author: b8horpet


import math


class Vector2D:
    Dimension = 2

    def __init__(self, _x: float = 0.0, _y: float = 0.0):
        self.x = _x
        self.y = _y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self

    def __rmul__(self, other):
        return Vector2D(self.x*other, self.y*other)

    def __truediv__(self, other):
        return Vector2D(self.x/other, self.y/other)

    def __itruediv__(self, other):
        self.x/=other
        self.y/=other
        return self

    def __rtruediv__(self, other):
        raise NotImplementedError()

    def __abs__(self):
        return math.sqrt(self * self)

    def __len__(self):
        return 2

    def __pow__(self, power, modulo = None):
        raise NotImplementedError()


class Vector3D(Vector2D):
    Dimension = 3

    def __init__(self, _x: float = 0.0, _y: float = 0.0, _z: float = 0.0):
        Vector2D.__init__(self, _x, _y)
        self.z = _z

    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __sub__(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        self.z *= other
        return self

    def __rmul__(self, other):
        return Vector3D(self.x*other, self.y*other, self.z*other)

    def __truediv__(self, other):
        return Vector3D(self.x/other, self.y/other, self.z/other)

    def __itruediv__(self, other):
        self.x/=other
        self.y/=other
        self.z/=other
        return self

    def __rtruediv__(self, other):
        raise NotImplementedError()

    def __len__(self):
        return 3

    def __pow__(self, power, modulo=None):
        return Vector3D(
            self.y*power.z-self.z*power.y,
            self.z*power.x-self.x*power.z,
            self.x*power.y-self.y*power.x
        )