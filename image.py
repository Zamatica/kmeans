
import cv2
import point


class Image:
    def __init__(self, filename) -> None:
        self.image = cv2.imread(filename=filename)
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def at(self, x, y):
        return self.image[x, y]

    def at_point(self, point: point.Point3D):
        return self.image[point.x, point.y]

    def at_gray(self, x, y):
        return self.gray[x, y]

    def at_gray_point(self, point: point.Point3D):
        return self.gray[point.x, point.y]
