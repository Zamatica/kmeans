#!/usr/bin/python3

import sys

import image
import kmeans_image

def help_screen():
    print(" Invalid Command Usage:")
    print("   main.py <k> <iterations> <image_file>")
    print("                k -- number of clusters")
    print("       iterations -- number of convergence iterations")
    print("       image_file -- directory path to image")
    exit(1)

def main():

    if len(sys.argv) < 4:
        help_screen()

    k = int(sys.argv[1])
    iterations = int(sys.argv[2])
    image_file = sys.argv[3]

    img = image.Image(image_file)
    img.read()

    gen = kmeans_image.KMeansImage(k, iterations, img)

    gen.execute()


if __name__ == "__main__":
    main()
