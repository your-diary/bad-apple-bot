#!/usr/bin/env python3

#-------------------------------------#

### import ###

import json

import cv2 

#-------------------------------------#

### Parameters ###

config_file: str = './config.json'

with open(config_file) as f:
    prm: dict = json.load(f)

target_video: str = prm['target_video']

frame_directory: str = prm['frame_directory']

fps: int = prm['fps']

#-------------------------------------#

### Functions ###

def video_to_frames(video_path): 
    
    video_object: object = cv2.VideoCapture(video_path) 
    
    count: int = 0
    
    success: int = 1
  
    while (True):

        count += 1
        print(f'{count} ({count / fps:.1f}s)')
  
        success, image = video_object.read() 

        if (not success):
            break

        output_file: str = f'{frame_directory}/frame_{count:05d}.jpg'
  
        success: bool = cv2.imwrite(output_file, image)
        if (not success):
            break
  
#-------------------------------------#

### main ###

if (__name__ == '__main__'): 

    video_to_frames(target_video)

#-------------------------------------#

