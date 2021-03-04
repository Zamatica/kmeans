
import cv2
import numpy as np
import color_class

# https://blog.paperspace.com/speed-up-kmeans-numpy-vectorization-broadcasting-profiling/
#    Mine was terrible slow, so i updated it with this. It's like cocaine


# Create count of how many times each pixel is assigned to a centroid
#    Use this count as a % of often it is added
#    Generate a picture based off the final %s

np.random.seed(4)

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
        def sort_centroids(centroids):
            n = len(centroids)
            for i in range(n):
                for j in range(0, n - 1):
                    gray_scale_j = 0.2126 * centroids[j][0] + 0.7152 * centroids[j][1] + 0.0722 * centroids[j][2]
                    gray_scale_j2 = 0.2126 * centroids[j + 1][0] + 0.7152 * centroids[j + 1][1] + 0.0722 * centroids[j + 1][2]

                    if gray_scale_j2 < gray_scale_j:
                        for k in range(len(centroids[j])):
                            centroids[j][k], centroids[j + 1][k] = centroids[j + 1][k], centroids[j][k]

        centroids = np.random.randint(0, 255, size=(self.k, 3))

        #centroids = []
        #for j in range(self.k):
        #    centroid = self.img.image[np.random.randint(self.img.image.shape[0])][np.random.randint(self.img.image.shape[1])]
        #    centroids.append(centroid)
#
        #centroids = np.array(centroids)

        sort_centroids(centroids)

        print(centroids)

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
