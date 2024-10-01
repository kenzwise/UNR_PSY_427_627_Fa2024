#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 19:05:03 2024

@author: mackenziewise
"""
#Code for Assignment 2. This code runs an experiment that presents blocks of faces (adults and childrent),
#places (house and corridors), and objects (instruments and cars). Each block is presented twice, once to the left 
#of a fixation cross and again to the right of a fixation cross. 

#I tried to eliminate as many magic numbers as possible and get this to run as a real experiment. 
#One thing that I think might be cool to add is a hidden "tab" option that the experimenter can use
#to skip to another block. Didn't add this, but considering it. 

#%% Set-up Imports
# Dealing with paths
from pathlib import Path
import random
#Experiment
from psychopy import visual, core, sound, event
import numpy as np

#%% Set parameters
# Set the path to directory
directory_path = Path('/Users/mackenziewise/Documents/Python/PSY 627/')

# Specify the images folder within the directory
images_folder = directory_path / 'fLoc_stimuli'

#Stimui Parameters
image_duration = 1.0        # 1 second per image
gap_duration = 0.25         # 0.25 second between images
block_duration = 20.0       # 20 seconds per block
preparation_duration = 3.0  # 3 seconds for preparation screen
screen_x = 800              # width of screen
screen_y = 400              # height of screen
stim_x = 200                # width of stimulus
stim_y = 200                # height of stimulus
fix_size = 20               # size of fixation cross
fix_pos = (0, 0)            # position of fixation cross
x_shift = 150               # x-pixels for left and right
y_shift = 0                 # y-pixels for center
back_color = (0.5, 0.5, 0.5)  # window background color 
sound_pitch = 500           # beep pitch
sound_dur = 0.1             # beep duration


#%% Load images and gather categories
image_files = [str(f) for f in images_folder.iterdir() if f.suffix.lower() in ['.png', '.jpg', '.jpeg']]

# Categorize images based on their filenames 
#note to self: using .lower() ensures that searching for files is not case-dependent (I believe).
faces_images = [f for f in image_files if "adult" in f.lower() or "child" in f.lower()]
places_images = [f for f in image_files if "corridor" in f.lower() or "house" in f.lower()]
objects_images = [f for f in image_files if "car" in f.lower() or "instrument" in f.lower()]

# Shuffle the images in each folder to be randomized 
random.shuffle(faces_images)
random.shuffle(places_images)
random.shuffle(objects_images)

#%% Setup PsychoPy window
win = visual.Window(size=(screen_x, screen_y), color=back_color, units='pix')

# Now setup the image stimulus size, the fixation cross, and the beep tone for the experiment. 
image_stim = visual.ImageStim(win, size=(stim_x, stim_y))  # Image size set to 100x100 pixels to ensure it's always square
fixation = visual.ShapeStim(win, vertices='cross', size=fix_size, lineColor='black', fillColor='black', pos=fix_pos)  # Fixation cross size in pixels
beep = sound.Sound(sound_pitch, secs=sound_dur)  # A short beep sound of 0.1 second duration

## Instructions & Screen Messages:
welcome_text = (
    "Hi there! Thank you for participating in this experiment.\n\n"
    "You will see a series of images on the screen.\n\n" 
    "Press any key to continue.")
    
instructions_text = (
    "Images will display either to the left or right side of a central fixation cross.\n\n"
    "Please keep your eyes on the fixation cross throughout the experiment.\n\n"
    "Press any key to begin." )

break_text = (
    "Break! You can take as long as you need, press any key to continue on.")

end_text = (
    "All done! Please notify the experimenter. \n\n"
    "Thank you for your time. Press any key to close this window.")

#Set-up how the messages will display on the screen:
instructions1 = visual.TextStim(win, text=welcome_text, color='black', height=20, wrapWidth=700, units='pix')
instructions2 = visual.TextStim(win, text=instructions_text, color='black', height=20, wrapWidth=700, units='pix')
instructions3 = visual.TextStim(win, text=break_text, color='black', height=20, wrapWidth=700, units='pix')
instructions4 = visual.TextStim(win, text=end_text, color='black', height=20, wrapWidth=700, units='pix')


#%% Function to present welcome text and instructions
def present_instructions():
    instructions1.draw()    # draw instructions 1 "welcome text"
    win.flip()              # flip to show
    event.waitKeys()        # Wait for any key press to continue
    instructions2.draw()    # draw instructions 2 "instructions text"
    win.flip()              # flip to show
    event.waitKeys()        # Wait for any key press to continue and start experiment


#%% Function to present preparation screen with fixation cross
def present_preparation_screen():
    fixation.draw()         # draw the fixation cross
    win.flip()              # flip to show
    core.wait(preparation_duration)  # Wait for 3 seconds then the experiment will begin

#%% Function to present break screen 
def present_break_screen():
    instructions3.draw()    # draw the break screen instructions
    win.flip()              # flip to show
    event.waitKeys()        # wait for any key press to continue

#%% Function to present end screen
def present_end_screen():
    instructions4.draw()   # draw the end of experiment text     
    win.flip()             # flip to show
    event.waitKeys()       # wait for any key press to close out the experiment

#%% Function to present a block of images
#this function simplifies things during the experiment, it will be called during each block. 

def image_presentation(images, position):
    start_time = core.getTime()
    while core.getTime() - start_time < block_duration:
        for image_path in images:
            if core.getTime() - start_time >= block_duration:
                break
            
            # Play beep sound
            beep.play()
            
            # Draw fixation point and image on screen
            fixation.draw()
            image_stim.image = image_path
            image_stim.pos = position
            image_stim.draw()
            win.flip()
            core.wait(image_duration)

            # Gap between images - show fixation only
            fixation.draw()
            win.flip()
            core.wait(gap_duration)

#%% Run! 

#1: Present instructions before the experiment
present_instructions()

#2: Present preparation screen before the first block starts
present_preparation_screen()

#3: Experiment loop
for repeat in range(2):  # Two repeats: first on the left, then on the right
    position = (-x_shift, y_shift) if repeat == 0 else (x_shift, y_shift)  # Left or right position in pixels

    # Present Faces block
    print("Presenting Faces Block")
    image_presentation(faces_images, position)
    present_preparation_screen()
    
    # Present Places block
    print("Presenting Places Block")
    image_presentation(places_images, position)
    present_preparation_screen()

    # Present Objects block
    print("Presenting Objects Block")
    image_presentation(objects_images, position)
    
    if repeat == 0:
        #Present Break text
        present_break_screen()
        present_preparation_screen()

    else:
            #Present End Text
            present_end_screen()

    
# Cleanup
win.close()
core.quit()

#if frozen, in the console enter control-c and/or control-d
