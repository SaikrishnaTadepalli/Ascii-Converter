import argparse
import math
from PIL import Image, ImageDraw, ImageFont

ASCII_CHARS = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@', 'M', 'W', '&', '$', 'X', 'A', 'O', 'K', 'B', '8']


def ResizeImage(original_image):
    return 0

def ConvertToAscii(image_path):
    original_image = Image.open(image_path)
    original_width, original_height = original_image.size

    resized_image = ResizeImage(original_image)
    resized_width, resized_height = resized_image.size

    pass



if __name__ == '__main__':
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Convert an image to ASCII art.')
    parser.add_argument('image_path', type=str, help='the path to the image file')
    args = parser.parse_args()

    # Convert the image to ASCII art
    ConvertToAscii(args.image_path)