#NOTE: This script is currently designed to generate arrays for two conditions (e.g., Happy/Sad, Black/White, etc)

import os
import glob
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from time import sleep

matplotlib.use('Agg')

## These directories should be changed to reflect locations on your local machine
# Stim Pool 1
hispanicFaces = (glob.glob("/Users/IanFerguson 1/Documents/ACADEMIA/02_NYU/THESIS/03_Stimuli/01_Hispanic/*.jpg"))

# Stim Pool 2
whiteFaces = (glob.glob("/Users/IanFerguson 1/Documents/ACADEMIA/02_NYU/THESIS/03_Stimuli/02_White/*.jpg"))

# Output Directory
path = ("/Users/IanFerguson 1/Documents/ACADEMIA/02_NYU/THESIS/03_Stimuli/00_Arrays/")

## Main Function

def constructArray(hispanic, white, output):

    """
                *** Parameters ***
    Hispanic = Number of hispanic faces in the array
    White = Number of white faces in the array
    Output = Number of arrays that will be constructed
            There should be 12 total faces
    """

    counter = 1

    while (counter <= output):

        random.shuffle(hispanicFaces)
        random.shuffle(whiteFaces)

        # Image Pool
        faces_H = np.random.choice(hispanicFaces, size = hispanic, replace = False).tolist()
        faces_W = np.random.choice(whiteFaces, size = white, replace = False).tolist()

        faces = faces_H + faces_W
        random.shuffle(faces)

        # Array Constructor
        w = 10
        h = 10
        fig = plt.figure(figsize=(13, 9))
        col = 4
        row = 3
        faceIndex = 0

        for i in range(1, (col*row)+1):

            border = (615,85,615,250)                       # Setup parameters for image size
            face = Image.open(faces[faceIndex])             # Open image data for display in ensemble
            face = ImageOps.crop(face, border)              # Crop image using border parameters
            ax = fig.add_subplot(row, col, i)               # Push face to ensemble
            ax.set_xticks([])                               # Remove X and Y ticks
            ax.set_yticks([])
            ax.axis('off')
            plt.imshow(face)
            faceIndex += 1                                  # Iterate through selected faces

        fig.subplots_adjust(wspace = -0.6, hspace= 0, )
        filename = str(hispanic).zfill(2) + "_" + str(white).zfill(2) + "_" + "faceArray" + str(counter).zfill(3)
        fig.savefig(os.path.join(path, filename))
        plt.close()
        sleep(1)
        counter += 1

## Array Construction
# User inputs how many arrays will be output

outputVolume = int(input("Arrays to construct:\t\t"))

auto_H = 0
auto_W = 12

while auto_H <= 12:

    constructArray(auto_H, auto_W, outputVolume)

    auto_H += 1
    auto_W -= 1

## List of files for Mechanical Turk
# Outputs a .txt file for easy copy-paste into Mechanical Turk script
newStim = sorted(glob.glob(path + "/*.png"))
output = open("All_Faces.txt", 'w')
organizer = 0;

for face in newStim:
    organizer += 1

    output.write("'" + face[-22:] + "', ")
    if ((organizer / 4) == 0):
        output.write("\n")
    organizer += 1

output.close()
