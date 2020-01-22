import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
import os
from PIL import Image, ImageDraw

"""
this script creates a random circles on given images each with different color

tasks to fix on the script:
    1. each circle should be be unique color and a dict between color to class should be made
    2. each image should have a dict between index of circle to it's color
    3. may need additional file containing the pair (index(of the circle), label(of the circle))
"""

# path to the data - and a list of all the files in the root
root = r'/home/itamarg/Pictures/ToShai'
name_files = os.listdir(root)

# const variables
num_classes = 4
num_circles = np.random.randint(4, 20)
max_radius = 200
min_radius = 20

# random color for each class
color = [tuple(np.random.choice(range(256), size=3)) for _ in range(num_classes)]

for file_name in name_files:
    # read image file to PIL object
    image_file = os.path.join(root, file_name)
    img = Image.open(image_file)

    # get random values for the circles position and size
    x = np.random.rand(num_circles) * np.array(img).shape[1]
    y = np.random.rand(num_circles) * np.array(img).shape[0]

    radius = np.random.rand(num_circles) * (max_radius - min_radius) + min_radius

    # create the drawing object on the img
    draw = ImageDraw.Draw(img)

    # Now, loop through coord arrays, and draw a circle at each x,y pair
    for xx, yy, rr, ccolor in zip(x, y, radius, color):
        draw.ellipse((xx - rr, yy - rr, xx + rr, yy + rr), fill=ccolor)
        draw.point((100, 100), 'red')

    # plot image
    img.show()
    # Save the image
    # image.save('test.png')
