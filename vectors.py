from math import cos, sin, radians


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, multiplier):
        return Vector(self.x * multiplier, self.y * multiplier)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def magnitude(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __str__(self):
        return str(self.x) + ", " + str(self.y)

    def dot(self, other):
        return self.x * other.x + self.y * other.y


    def rotate(self, angle):
        angle = radians(angle)
        return Vector(self.x * cos(angle) - self.y * sin(angle), self.x * sin(angle) + self.y * cos(angle))

    def coordinates(self):
        return (self.x, self.y)


null_vector = Vector(0, 0)

def unit_vector(angle):
    return Vector(cos(radians(angle)),
                  sin(radians(angle)))