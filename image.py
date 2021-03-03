
import cv2
import point

class Color:
    def __init__(self, red=0, green=0, blue=0) -> None:
        self.red = red
        self.green = green
        self.blue = blue

    def distance(self, red, green, blue) -> int:
        return (self.red - red) * (self.red - red) + \
               (self.green - green) * (self.green - green) + \
               (self.blue - blue) * (self.blue - blue)

    def to_rgb_tuple(self) -> tuple:
        return (self.red, self.green, self.blue)

    def to_bgr_tuple(self) -> tuple:
        return (self.blue, self.green, self.red)

    def from_hsv(self, hue, saturation, brightness) -> None:
        if saturation == 0.0:
            self.red = brightness
            self.green = brightness
            self.blue = brightness
        
        i = int(hue * 6.)
        f = (hue * 6.) - i
        
        p = brightness * (1. - saturation)
        q = brightness * (1. - saturation * f)
        t = brightness * (1. - saturation * (1. - f))
        
        i %= 6
        
        if i == 0:
            self.red = brightness
            self.green = t
            self.blue = p
        elif i == 1:
            self.red = q
            self.green = brightness
            self.blue = p
        elif i == 2:
            self.red = p
            self.green = brightness
            self.blue = t
        elif i == 3:
            self.red = p
            self.green = q
            self.blue = brightness
        elif i == 4:
            self.red = t
            self.green = p
            self.blue = brightness
        elif i == 5:
            self.red = brightness
            self.green = p
            self.blue = q


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
