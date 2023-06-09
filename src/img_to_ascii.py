import argparse
import math
import os
from PIL import Image, ImageDraw

ASCII_CHARS = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@', 'M', 'W', '&', '$', 'X', 'A', 'O', 'K', 'B', '8']

# Width and Height of Font in Pixels
FONT_WIDTH = 8
FONT_HEIGHT = 12

FONT_RATIO = FONT_WIDTH / FONT_HEIGHT
SCALE_FACTOR = 0.4

def GetOutputTextName(image_path):
    input_file_name = os.path.basename(image_path)
    return input_file_name.split('.')[0] + '-ascii.txt'

def GetOutputImageName(image_path):
    input_file_name = os.path.basename(image_path)
    return input_file_name.split('.')[0] + '-ascii.' + input_file_name.split('.')[1]

# IMPLEMENT Lanczos resize algorithm here.
def ResizeImage(original_image, scale_factor):
    image_width, image_height = original_image.size

    return original_image.resize(
        (
            int(scale_factor * image_width),
            int(scale_factor * FONT_RATIO * image_height)
        ),
        Image.NEAREST
    )

def GetCharacter(grey_val):
    char_index = math.floor(grey_val * len(ASCII_CHARS) / 256)
    return ASCII_CHARS[char_index]

def ImageToAscii(original_image, image_path='input.jpg', output_folder='./'):
    resized_image = ResizeImage(original_image, SCALE_FACTOR)
    resized_width, resized_height = resized_image.size

    output_text = open(output_folder + '/' + GetOutputTextName(image_path), 'w')
    output_image = Image.new(
        'RGB',
        (FONT_WIDTH * resized_width, FONT_HEIGHT * resized_height),
        color=(0, 0, 0)
    )

    pixels = resized_image.load()
    drawer = ImageDraw.Draw(output_image)

    # Speed up here using Multithreading/Multiprocessing
    for i in range(resized_height):
        for j in range(resized_width):
            r, g, b = pixels[j, i]

            ascii_char = GetCharacter(int((r + g + b) / 3))

            output_text.write(ascii_char)
            drawer.text(
                (FONT_WIDTH * j, FONT_HEIGHT * i),
                ascii_char,
                fill=(r, g, b)
            )
        output_text.write('\n')
    
    output_image.save(output_folder + '/' + GetOutputImageName(image_path))

def ConvertToAscii(image_path):
    original_image = Image.open(image_path)
    ImageToAscii(original_image, image_path)

if __name__ == '__main__':
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Convert an image to ASCII.')
    parser.add_argument('image_path', type=str, help='the path to the image file')
    args = parser.parse_args()

    # Convert the image to ASCII art
    ConvertToAscii(args.image_path)