
import cv2
import numpy as np
import image
import color_class

# https://blog.paperspace.com/speed-up-kmeans-numpy-vectorization-broadcasting-profiling/
#    Mine was terrible slow, so i updated it with this. It's like cocaine


# Create count of how many times each pixel is assigned to a centroid
#    Use this count as a % of often it is added
#    Generate a picture based off the final %s

#np.random.seed(4)

class Centroid:
    def __init__(self, color) -> None:
        self.color = color

class KMeansImage:
    def __init__(self, k, iterations, image):
        self.k = k
        self.iterations = iterations

        self.centroids = []
        self.assigned_centroids = np.zeros(image.image.shape[0] * image.image.shape[1], dtype = np.int32)
        self.colors = []

        self.img = image
        self.output = np.empty(self.img.image.shape)
        self.output = self.output.reshape((-1, 3))


    # Runs kMeans on the stored image
    def execute(self):
        centroids = self.build_centroids()

        img1d = self.img.image.reshape((-1, 3))

        for n in range(self.iterations):
            self.assignment(img1d[:, None, :], centroids[None, :, :])

            for centroid_index in range(centroids.shape[1]):
                cluster_data = img1d[self.assigned_centroids == centroid_index]

                new_centroid = cluster_data.mean(axis = 0)

                centroids[centroid_index] = new_centroid

        for i in range(len(self.assigned_centroids)):
            self.output[i] = self.colors[self.assigned_centroids[i]].to_bgr()

        self.write_images()


    def write_images(self):
        cv2.imwrite("out.jpg", self.output.reshape(self.img.image.shape))


    def build_centroids(self):
        centroids = np.random.randint(0, 255, size=(self.k, 3))

        for i in range(self.k):
            color = color_class.Color()
            color.from_hex_index(i)

            self.colors.append(color)

        return centroids


    def assignment(self, img1d, centroids):
        distance = ((img1d - centroids) ** 2).sum(axis = img1d.ndim - 1)

        self.assigned_centroids = np.argmin(distance, axis = 1)
