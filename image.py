
import cv2
import point


class Image:
    def __init__(self, filename) -> None:
        self.image = None
        self.gray = None
        
        self.filename = filename

    # ---------- Reads ---------- #

    def read(self):
        self.image = cv2.imread(self.filename)
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)


    # ---------- Writes ---------- #
    # (B, G, R)

    def write(self, file=None):
        file = file | self.filename
        cv2.imwrite(self.filename, self.image)

    def write_gray(self, file=None):
        file = file | self.filename
        cv2.imwrite(file, self.gray)


    # ---------- Access ---------- #

    def at(self, x, y):
        return self.image[x, y]

    def at_point(self, point: point.Point3D):
        return self.image[point.x, point.y]

    def at_gray(self, x, y):
        return self.gray[x, y]

    def at_gray_point(self, point: point.Point3D):
        return self.gray[point.x, point.y]
