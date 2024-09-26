#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on Tue Sep 10 13:23:21 2024

#@author: mackenziewise
# 16SEPT2024
# PS 627
# Code Assignment #1 

#%% Set-up Imports
# Imports
# Dealing with array data
import numpy as np
# Dealing with paths
import pathlib
from pathlib import Path
import glob
import os
# To load and show images
import matplotlib.pyplot as plt
import PIL
from PIL import Image
# Alternative to load arrays
import h5py
import random


#%% 1. Create a sorted list of all images in that folder.
#Set up working directory
# Set the path to directory
directory_path = Path('/Users/mackenziewise/Documents/Python Docs/PSY 627/')

# Specify the images folder within the directory
images_folder = directory_path / 'fLoc_stimuli'

# Check if the images folder exists
if not images_folder.is_dir():
    print(f"The directory {images_folder} does not exist.")
else:
    # List all image files in the folder (adjust the patterns for your image types)
    image_files = list(images_folder.glob('*.jpg')) + list(images_folder.glob('*.png'))

    # Sort the list of image files by name
    sorted_image_files = sorted(image_files, key=lambda x: x.name)

    # Store the sorted file names in a list
    sorted_image_names = [image_file.name for image_file in sorted_image_files]

    # Print the sorted list of image filenames
    print("Sorted list of images:")
    for image_name in sorted_image_names:
        print(image_name)


#%% 2. Select a random sample of 12 images.
   
 # Select a random sample of 12 images from the sorted list
    random_images = random.sample(sorted_image_files, 12)

    # Get the names of the random images
    random_image_names = [image_file.name for image_file in random_images]

    # Print the random sample of 12 images
    print("\nRandom sample of 12 images:")
    for image_name in random_image_names:
        print(image_name)

#%% 3. Display each of the 12 randomly chosen images sequentially (in your random order)  
# * in the same figure, but not as a subplot or grid (meaning replace the image in a figure over and over to display all 12*
# This is sort of a starter version of loading and showing images for an experiment.

    # Create a figure window
    plt.figure()

    # Loop through each image
    for image_file in random_images:
        # Load the image
        img = Image.open(image_file)
       
        # Convert the image to grayscale
        img_gray = img.convert('L')

        # Clear the current figure
        plt.clf()

        # Display the grayscale image
        plt.imshow(img_gray, cmap='gray')
        plt.axis('off')  # Hide axes

        # Draw the canvas
        plt.draw()

        # Pause to display the image for a certain amount of time (e.g., 2 seconds)
        plt.pause(0.25)

    # Close the figure window after displaying all images
    plt.close()


#%% 4. Concatenate the images into an array and save them as one big array in 
# an appropriate file called 'randomly_selected_images' 
# (with appropriate extension for however you are saving them). 
# The resulting array should have one dimension that is 12 long (one for each image)
# Initialize a list to store the image arrays
image_arrays = []

# Optional: Define a common size for all images (uncomment if resizing is needed)
# common_size = (256, 256)  # For example

# Loop through each image
for image_file in random_images:
    # Load the image
    img = Image.open(image_file)

    # Convert the image to grayscale
    img_gray = img.convert('L')

    # Optional: Resize the image to the common size (uncomment if resizing is needed)
    # img_gray = img_gray.resize(common_size)

    # Convert the image to a numpy array
    img_array = np.array(img_gray)

    # Append the array to the list
    image_arrays.append(img_array)

# Stack the image arrays along a new dimension
concatenated_images = np.stack(image_arrays, axis=-1)  # Stack along the last axis

# Save the concatenated array to a file called 'randomly_selected_images.npy'
np.save('randomly_selected_images.npy', concatenated_images)

#%% Graduate students:
# In addition to the above, make a figure with subplots to display each of the 
# 12 images in a 4 x 3 'light table" grid. (We have not covered how to do this! 
# but remember, this is OPEN CHATBOT).

# Create a new figure
plt.figure(figsize=(12, 9))  # Adjust the figure size as needed

# Loop through each image and add it to a subplot
for idx, image_file in enumerate(random_images):
    # Load the image
    img = Image.open(image_file)

    # Convert the image to grayscale
    img_gray = img.convert('L')

    # Add a subplot in a 4x3 grid
    plt.subplot(3, 4, idx + 1)  # idx + 1 because subplot indices start at 1

    # Display the grayscale image
    plt.imshow(img_gray, cmap='gray')
    plt.axis('off')  # Hide axes

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the figure
plt.show()

