import subprocess
import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance

call = lambda x: subprocess.check_call(x, shell=True)

apath = lambda path: os.path.abspath(path)


input_path = "./tmp/pics/1.jpeg"
out_dir = "./tmp/pics/out"


def clear():
    if not len(os.listdir(apath(out_dir))):
        return

    command = f"rm {apath(out_dir)}/*"
    print(call(command))


def modify_brightness(input_image_path, output_image_path, brightness_factor):
    try:
        # Open the image
        image = Image.open(input_image_path)

        # Create an enhancer object for brightness
        enhancer = ImageEnhance.Brightness(image)

        # Modify the brightness using the factor provided
        modified_image = enhancer.enhance(brightness_factor)

        # Save the modified image to the output path
        modified_image.save(output_image_path)

        print("Brightness modification successful!")
    except Exception as e:
        print(f"Error: {e}")


clear()

total = 10
wing = 10
x = 0

for i in range(total):
    x += 1 / total * 2.5
    out_path = f"{out_dir}/{i}_{str(x)[:5]}.jpeg"

    modify_brightness(input_path, out_path, x)
