import argparse
import math
import os
from PIL import Image, ImageDraw, ImageFont

ASCII_CHARS = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@', 'M', 'W', '&', '$', 'X', 'A', 'O', 'K', 'B', '8']

FONT_WIDTH = 1
FONT_HEIGHT = 2

FONT_RATIO = int(FONT_WIDTH / FONT_HEIGHT)
SCALE_FACTOR = 0.2

def GetOutputTextName(image_path):
    input_file_name = os.path.basename(image_path)
    return input_file_name.split('.')[0] + '-ascii.txt'

def GetOutputImageName(image_path):
    input_file_name = os.path.basename(image_path)
    return input_file_name.split('.')[0] + '-ascii.' + input_file_name.split('.')[1]

def ResizeImage(original_image, scale_factor):
    image_width, image_height = original_image.size

    return original_image.resize(
        (
            int(scale_factor * image_width),
            int(scale_factor * FONT_RATIO * image_height)
        ),
        Image.NEAREST
    )

def ConvertToAscii(image_path):
    

    original_image = Image.open(image_path)
    original_width, original_height = original_image.size

    resized_image = ResizeImage(original_image, SCALE_FACTOR)
    resized_width, resized_height = resized_image.size

    output_text = open(GetOutputTextName(image_path), 'w')
    output_image = 0

    drawer = ImageDraw.Draw(output_image)

    # DRAW

    output_image.save(GetOutputImageName(image_path))



if __name__ == '__main__':
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Convert an image to ASCII art.')
    parser.add_argument('image_path', type=str, help='the path to the image file')
    args = parser.parse_args()

    # Convert the image to ASCII art
    ConvertToAscii(args.image_path)