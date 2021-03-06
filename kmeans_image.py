
import cv2
import numpy as np
import warnings
import color_class

# Hide Warnings about empty clusters
np.seterr(divide='ignore', invalid='ignore')

# https://blog.paperspace.com/speed-up-kmeans-numpy-vectorization-broadcasting-profiling/
#    Mine was terrible slow, so i updated it with this. It's like cocaine


# Create count of how many times each pixel is assigned to a centroid
#    Use this count as a % of often it is added
#    Generate a picture based off the final %s


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

        self.count_output = np.zeros((self.img.image.shape[0] * self.img.image.shape[1], self.k))


    # Runs kMeans on the stored image
    def execute(self):
        centroids = self.build_centroids()

        img1d = self.img.image.reshape((-1, 3))

        for n in range(self.iterations):
            sse = 0

            self.assignment(img1d[:, None, :], centroids[None, :, :])

            self.update_count()

            # Ignore Warnings from Empty Clusters
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)

                for centroid_index in range(centroids.shape[0]):
                    cluster_data = img1d[self.assigned_centroids == centroid_index]
                    new_centroid = cluster_data.mean(axis = 0)

                    centroids[centroid_index] = new_centroid
            
            sse = ((img1d - centroids[self.assigned_centroids]) ** 2).sum() / len(img1d)
            if sse < 0.5:
                break

        for i, centroid_index in enumerate(self.assigned_centroids):
            self.output[i] = centroids[centroid_index]

        self.write_images()


    def write_images(self):
        cv2.imwrite("output/kmeans-centroid.jpg", self.output.reshape(self.img.image.shape))

        for i, centroid_index in enumerate(self.assigned_centroids):
            self.output[i] = self.colors[centroid_index].to_bgr()
        cv2.imwrite("output/kmeans-contrast.jpg", self.output.reshape(self.img.image.shape))

        for k in range(self.k):
            output_data = np.zeros((self.img.gray.shape[0] * self.img.gray.shape[1],))

            for i in range(len(self.count_output)):
                pixel_cluster_count = self.count_output[i][k]

                output_data[i] = int((float(pixel_cluster_count) / self.iterations) * 255)

            cv2.imwrite("output/out-k" + str(k) + ".jpg", output_data.reshape(self.img.gray.shape))


    def update_count(self):
        for i, centroid_index in enumerate(self.assigned_centroids):
            self.count_output[i][centroid_index] += 1


    def build_centroids(self):
        def build_centroid(gray_scale):
            red = 0
            green = 0
            blue = -1

            while not (0 <= blue <= 255):
                red = np.random.randint(0, 255)
                green = np.random.randint(0, 255)
                blue = int((gray_scale - (red * 0.3 + green * 0.59)) / 0.11)

            return [red, blue, green]
            
        centroids = []
        gray_scale = 0
        step = int(255 / self.k)
        for _ in range(self.k):
            centroids.append(build_centroid(gray_scale))
            gray_scale += step
        centroids = np.array(centroids)

        for i in range(self.k):
            color = color_class.Color()
            color.from_hex_index(i)

            self.colors.append(color)

        return centroids


    def assignment(self, img1d, centroids):
        distance = ((img1d - centroids) ** 2).sum(axis = img1d.ndim - 1)

        self.assigned_centroids = np.argmin(distance, axis = 1)
        #print(distance)
        #print(np.argmin(distance, axis = 1))
        #input()
