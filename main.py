
import cv2

import image
import kmeans

def main():
    img = image.Image("images/random.jpg")
    img.read()

    gen = kmeans.KMeansImage(5, 50, img)

    gen.execute()


if __name__ == "__main__":
    main()
