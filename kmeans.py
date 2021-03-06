#!/usr/bin/python3

import sys

import image
import kmeans_image

import numpy as np

def help_screen():
    print(" Invalid Command Usage:")
    print("   kmeans.py <k> <iterations> <image_file> [SEED]")
    print("                k -- number of clusters")
    print("       iterations -- number of convergence iterations")
    print("       image_file -- directory path to image")
    print("             SEED -- seeds the numpy generation (defaults to random)")
    exit(1)

def main():

    if len(sys.argv) < 4:
        help_screen()

    SEED = np.random.randint(9999999)
    if len(sys.argv) > 4:
        SEED = int(sys.argv[4])

    np.random.seed(SEED)
    print("SEED = " + str(SEED))

    k = int(sys.argv[1])
    iterations = int(sys.argv[2])
    image_file = sys.argv[3]

    img = image.Image(image_file)
    img.read()

    gen = kmeans_image.KMeansImage(k, iterations, img)

    gen.execute()


if __name__ == "__main__":
    main()
