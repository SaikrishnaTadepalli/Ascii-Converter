import argparse
import math
import os
from PIL import Image, ImageDraw
import cv2
import moviepy.editor as mp


def ConvertToAscii(video_path):
    print('Hello, World2!')

if __name__ == '__main__':
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Convert an video to ASCII.')
    parser.add_argument('video_path', type=str, help='the path to the video file')
    args = parser.parse_args()

    # Convert the image to ASCII art
    ConvertToAscii(args.video_path)