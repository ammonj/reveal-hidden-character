#!/usr/bin/env python3

import json
import math
import glob

def loadCharacters(file_path):
    character_set = []
    with open(file_path, mode='r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for c in data:
            char = c[1][0]
            val = c[1][1]
            if val is not None: #removes characters with invalid data
                val = float(val) #converts value datastring to float type
                character_set.append(c)
    return character_set
    
def typeCharacter(letter, wght_value):
    font(font_name, font_size)
    fill(1, 1, 1)

    wght_value = float(wght_value) * 10
    wght_value = round(wght_value)

    fontVariations(wght=wght_value)
    text(letter, (w/15, vertical_pos))
    
    translation_value = textSize(letter)[0]
    return translation_value

def getTotalSteps(characterlist):
    steps = 0
    for c in character_data:
        steps += float(c[1][1])
    return int(steps)
    
def createAnimation(name):
    
    newDrawing() # reset the drawing stack
    
    total_steps = getTotalSteps(character_data)
    print("total steps:", total_steps)

    steps_per_frame = steps_per_second * frame_duration
    print("steps per frame:", steps_per_frame)

    total_frames = total_steps / steps_per_frame
    print("total frames:", total_frames)
    
    if total_frames == 0: #stop function if there are no frames (edge case)
        return

    min_var = listFontVariations(font_name)['wght']['minValue']

    cc = 0 # current character
    current_val = min_var # current value
    translation_value = 0

    # for each frame...
    for frame in range(int(total_frames)):
        # create a new page and set its duration
        newPage(w, h)
        frameDuration(frame_duration)
        # draw the background rectangle
        fill(0.1, 0.1, 0.1)
        rect(0,0,w,h)
        
        if cc < len(character_data): # draw only if characters are left


            for c in character_data:
                char = c[1][0]
                if character_data.index(c) < cc:
                    end_val = c[1][1]
                    translation_value = typeCharacter(char, end_val)
                    translate(translation_value,0)
                if character_data.index(c) == cc:
                    if current_val >= float(c[1][1]):
                        if current_val > float(c[1][1]):
                            current_val = float(c[1][1])
                        translation_value = typeCharacter(char, current_val)
                        translate(translation_value,0)
                        cc += 1
                        current_val = min_var # current value
                    else:
                        translation_value = typeCharacter(char, current_val)
                        translate(translation_value,0)
                        current_val += steps_per_frame
                        
            
    # save the animation as a 
    filename = "%s.mp4" % name
    saveImage(filename, imageResolution=144)
    print ("saved mp4 for", filename)
    
    # save last frame as picture
    #filename = "%s.png" % name
    #saveImage(filename, imageResolution=144)
    #print ("saved png for", filename)


    
#### main

all_data_files = glob.glob('data/*.json')

font_path = "font.ttf"
font_name = installFont(font_path)

w, h = 500, 100

font_size = 30

y = int(h / 2)
f = font_size / 4
vertical_pos = y - f

# parameters for animation speed
steps_per_second = 150
frame_duration = 0.05

for data_file in all_data_files:
    file_name = str(data_file)
    if glob.glob(file_name): # check if current file really exists
        character_data = loadCharacters(data_file)
        print("create animation for file", data_file)
        createAnimation(file_name)
    
uninstallFont(font_path)