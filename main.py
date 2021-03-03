
import cv2

import image
import kmeans

def main():
    img = image.Image("images/hand.jpeg")
    img.read()

    gen = kmeans.KMeansImage(4, img)

    gen.execute()


if __name__ == "__main__":
    main()
