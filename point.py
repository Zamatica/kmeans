
import numpy as np

class Point3D:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.z = 0

    def distance(self, point: 'Point3D') -> float:
        return (self.x - point.x) * (self.x - point.x) + \
               (self.y - point.y) * (self.y - point.y) + \
               (self.z - point.z) * (self.z - point.z)

    def distance_sqrt(self, point: 'Point3D') -> float:
        return np.sqrt(self.distance(point))

