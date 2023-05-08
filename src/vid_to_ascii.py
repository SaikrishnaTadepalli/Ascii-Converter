import argparse
import os
import subprocess
from PIL import Image
import tempfile

# Import ImageToAscii from the previous file
from img_to_ascii import ImageToAscii

# Path to ffmpeg executable
FFMPEG_PATH = '/opt/homebrew/bin/ffmpeg'

# ASCII video dimensions (in characters)
ASCII_WIDTH = 120
ASCII_HEIGHT = 80

# Frame rate of the output ASCII video
OUTPUT_FPS = 30

# Temporary directory to store individual frames and audio file
TEMP_DIR = './tmp'

def ConvertVideoToAscii(input_video_path):
    # Create temporary directories for frames and audio
    frame_dir = tempfile.mkdtemp(dir=TEMP_DIR)
    audio_file = os.path.join(TEMP_DIR, 'audio.wav')

    # Use ffmpeg to extract frames from the video and save them as images in the frame directory
    ffmpeg_cmd = f'{FFMPEG_PATH} -i "{input_video_path}" -q:v 1 -r {OUTPUT_FPS} -f image2 "{frame_dir}/frame-%05d.jpg"'
    subprocess.call(ffmpeg_cmd, shell=True)

    # Use ffmpeg to extract audio from the video and save it as a wav file
    ffmpeg_cmd = f'{FFMPEG_PATH} -i "{input_video_path}" -vn -acodec pcm_s16le -ar 44100 -ac 2 "{audio_file}"'
    subprocess.call(ffmpeg_cmd, shell=True)

    # Open the audio file as binary and read its content
    with open(audio_file, 'rb') as f:
        audio_data = f.read()

    # Create a list of paths to all the image frames
    frame_paths = [os.path.join(frame_dir, f) for f in os.listdir(frame_dir) if f.endswith('.jpg')]
    frame_paths.sort()

    # Create a new directory for the ASCII frames
    ascii_frame_dir = tempfile.mkdtemp(dir=TEMP_DIR)

    # Convert each frame to ASCII and save the resulting image in the ASCII frame directory
    for i, frame_path in enumerate(frame_paths):
        print(f'Converting frame {i+1}/{len(frame_paths)}...')
        frame_image = Image.open(frame_path)
        ImageToAscii(frame_image, os.path.join(ascii_frame_dir, f'frame-{i:05}.jpg'), output_folder=ascii_frame_dir)

    # Use ffmpeg to combine the ASCII frames and the original audio into a single video file
    output_video_path = f'{input_video_path[:-4]}-ascii.mp4'
    ffmpeg_cmd = f'{FFMPEG_PATH} -framerate {OUTPUT_FPS} -i "{os.path.join(ascii_frame_dir, "frame-%05d-ascii.jpg")}" -i "{audio_file}" -c:v libx264 -preset slow -crf 22 -c:a aac -b:a 192k -shortest "{output_video_path}"'
    subprocess.call(ffmpeg_cmd, shell=True)

    # Remove temporary directories and files
    os.remove(audio_file)
    for f in frame_paths:
        os.remove(f)
    for f in os.listdir(ascii_frame_dir):
        os.remove(os.path.join(ascii_frame_dir, f))
    os.rmdir(frame_dir)
    os.rmdir(ascii_frame_dir)

    print(audio_file)
    print(f'Output video saved to {output_video_path}')

if __name__ == '__main__':
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Convert a video to ASCII.')
    parser.add_argument('input_video_path', type=str, help='the path to the input video file')
    args = parser.parse_args()

    # Convert the video to ASCII art
    ConvertVideoToAscii(args.input_video_path)


# ffmpeg -framerate 30 -i ./tmp/tmp9072pfrh/frame-%05d-ascii.jpg -i ./tmp/audio.wav -c:v libx264 -preset slow -crf 22 -c:a aac -b:a 192k -shortest ./output.mp4
