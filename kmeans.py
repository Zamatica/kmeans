
import cv2
import numpy as np
import point
import image

# https://benalexkeen.com/k-means-clustering-in-python/


# Create count of how many times each pixel is assigned to a centroid
#    Use this count as a % of often it is added
#    Generate a picture based off the final %s


class Centroid:
    def __init__(self, color) -> None:
        self.color = color

class KMeansImage:
    def __init__(self, k, image):
        self.k = k
        self.centroids = []
        self.img = image
        self.output = np.zeros(self.img.image.shape, np.uint8)


    # Runs kMeans on the stored image
    def execute(self):
        centroids = self.build_centroids()

        self.assignment(centroids)

        self.write_images()


    def write_images(self):
        cv2.imwrite("out.jpg", self.output)


    def build_centroids(self):
        def generate_colors(count):
            colors = []
            for i in range(count):
                color = image.Color()
                color.from_hsv( (((i % 3) * count / 3) + (i / 3)) * 255.0 / count,
                               255,
                               128)
                colors.append(color)
            return colors

        centroids = []

        colors = generate_colors(self.k)

        for color in colors:
            centroids.append(Centroid(color))

        return centroids


    def assignment(self, centroids):
        for y in range(self.img.image.shape[0]):
            for x in range(self.img.image.shape[1]):
                pixel_value = self.img.image[y, x]
                
                min_distance = float('inf')
                centroid_index = -1
                for i, centroid in enumerate(centroids):
                    distance = centroid.color.distance(pixel_value[0], pixel_value[1], pixel_value[2])
                    
                    if distance < min_distance:
                        centroid_index = i
                        min_distance = distance

                self.output[y, x] = centroids[centroid_index].color.to_bgr_tuple()

