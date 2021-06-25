#!/usr/bin/env python3

#-------------------------------------#

### import ###

import glob
import json
import os
import pickle
import random
import sys
import time

import discord
from PIL import Image

#-------------------------------------#

### Parameters ###

config_file: str = './config.json'

with open(config_file) as f:
    prm: dict = json.load(f)

token: str = prm['token']

pickle_file: str = prm['pickle_file']

frame_directory: str = prm['frame_directory']

fps: int = prm['fps']

num_frame: int = len(glob.glob(f'{frame_directory}/*'))

if (num_frame == 0):
    print('No frame found.')
    sys.exit(1)

video_length_sec: int = num_frame * (1 / fps)

ascii_chars: list[str] = ['⠀', '⠄', '⠆', '⠖', '⠶', '⡶', '⣩', '⣪', '⣫', '⣾', '⣿']
ascii_chars.reverse() #TODO what?
ascii_chars = ascii_chars[::-1]

width: int = prm['new_width']

#This is the time length per frame.
#But the number of the frames are decreased by `/4` and the time length per frame is multiplied by `18`.
#I don't know why `18` was chosen.
timeout = 1 / ((int(num_frame / 4) + 1) / video_length_sec) * 18

#-------------------------------------#

### Functions ###

def resize(image: object, new_width: int) -> object:
    (old_width, old_height) = image.size
    aspect_ratio: float = old_height / old_width
    new_height: int = int((aspect_ratio * new_width) / 2) #why `/2`?
    new_dimension = (new_width, new_height)
    new_image: object = image.resize(new_dimension)
    return new_image

def grayscalify(image: object) -> object:
    return image.convert('L')

def convert_to_ascii_art(image: object, buckets = 25) -> str:
    initial_pixels = list(image.getdata())
    new_pixels = [ascii_chars[pixel_value // buckets] for pixel_value in initial_pixels] #A larger pixel value corresponds to a larger index for `ascii_chars: list[str]`.
    return ''.join(new_pixels) #returns an 1D string (1D means `without newline`)

def process_image(image: object, new_width: int = width) -> str:
    image: object = resize(image, new_width)
    image: object = grayscalify(image)
    pixels: str = convert_to_ascii_art(image)
    len_pixels: int = len(pixels)
    new_image: list[str] = [pixels[index : index + int(new_width)] for index in range(0, len_pixels, int(new_width))]
    return '\n'.join(new_image)

def process_frame(frame_path: str) -> str:
    try:
        image: object = Image.open(frame_path)
    except Exception:
        print(f"The frame [ {frame_path} ] doesn't exist.")
        sys.exit(1)
    return process_image(image)

print('Preparing frames...')
frames: list[str] = []
if (os.path.isfile(pickle_file)):
    with open(pickle_file, 'rb') as f:
        frames = pickle.load(f)
else:

    for i in range(1, int(num_frame / 4) + 1): #`/4` decreases the number of the frames.
        print(f'    {i:04d}/{int(num_frame / 4)}')
        frame_path: str = f'{frame_directory}/frame_{i * 4:05d}.jpg'
        frames.append(process_frame(frame_path))

#     #Use this instead and uncomment `sys.exit(0)` below if you'd like not to thin out any frames.
#     #This may be useful when used with `./terminal.py`.
#     for i in range(1, int(num_frame) + 1):
#         print(f'    {i:04d}/{int(num_frame)}')
#         frame_path: str = f'{frame_directory}/frame_{i:05d}.jpg'
#         frames.append(process_frame(frame_path))

    with open(pickle_file, 'wb') as f:
        pickle.dump(frames, f)

# sys.exit(0)

#-------------------------------------#

### Classes ###

class MyClient(discord.Client):

    async def on_connect(self) -> None:
        print('Connected.')
        print('Logging in...')

    async def on_disconnect(self) -> None:
        print('Disconnected')

    async def on_ready(self) -> None:
        print(f'Logged in as [ {self.user} ].')

    async def on_message(self, message):

        if (message.content.startswith('bad apple')):

            tokens: list[str] = message.content.split(' ')

            if (True):

                index: int = None

                if (len(tokens) == 3):
                    try:
                        index: int = int(tokens[2])
                    except:
                        pass

                if (index is None):
                    index = random.randint(0, len(frames))

                try:
                    ascii_art: str = frames[index]
                except:
                    index = random.randint(0, len(frames))
                    ascii_art: str = frames[index]

                await message.channel.send(f':green_apple: Bad Apple!! ({index:04d} / {len(frames)}) :apple:')
                await message.channel.send(ascii_art)

            else: #play mode

                unix_time_old: int = time.time()

                i = 0

                while (i < len(frames) - 1):

                    while (True):

                        time.sleep(0.1)

                        unix_time_new: int = time.time()

                        if ((unix_time_new - unix_time_old) >= timeout):

                            await message.channel.send(frames[int(i)])
                            
                            i += (unix_time_new - unix_time_old) / timeout
                            
                            unix_time_old = unix_time_new

                            break

#-------------------------------------#

### main ###

if (__name__ == '__main__'):

#     #plays on terminal
#     for i in range(len(frames)):
#         print(frames[i])
#         time.sleep(timeout / 18)

    try:
        client: object = MyClient()
        client.run(token)
    except BaseException as e:
        print(e)

#-------------------------------------#

