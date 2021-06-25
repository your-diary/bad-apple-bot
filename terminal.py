#!/usr/bin/env python3

#-------------------------------------#

### import ###

import json
import pickle
import time

#-------------------------------------#

### Parameters ###

config_file: str = './config.json'

with open(config_file) as f:
    prm: dict = json.load(f)

fps: int = prm['fps']

pickle_file: str = prm['pickle_file']

with open(pickle_file, 'rb') as f:
    frames: list[str] = pickle.load(f)

play_speed: float = 0.5
sec_per_frame: int = 1 / fps / play_speed

#-------------------------------------#

### main ###

if (__name__ == '__main__'):
    frame_number_old: int = 0
    num_frame: int = len(frames)
    t_start: int = time.time()
    while (True):
        time.sleep(sec_per_frame / 10)
        t: int = time.time() - t_start
        frame_number: int = int(t / sec_per_frame)
        if (frame_number != frame_number_old):
            if (frame_number == num_frame):
                break
            frame_number_old = frame_number
            print(frames[frame_number])
            print()

#-------------------------------------#

