
import numpy as np

class Point3D:
    def __init__(self, x = 0, y = 0, z = 0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def distance(self, point: 'Point3D') -> float:
        return (self.x - point.x) * (self.x - point.x) + \
               (self.y - point.y) * (self.y - point.y) + \
               (self.z - point.z) * (self.z - point.z)

    def distance_sqrt(self, point: 'Point3D') -> float:
        return np.sqrt(self.distance(point))


class Point1D:
    def __init__(self, val: int = 0) -> None:
        self.x = val

    def distance(self, point: 'Point1D'):
        return (self.x - point.x) * (self.x - point.x)

    def distance_sqrt(self, point: 'Point1D'):
        return np.sqrt(self.distance(point))

    def distance_number(self, p):
        return abs((self.x - p))
