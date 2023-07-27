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


from PIL import Image, ImageEnhance


def modify_contrast(input_image_path, output_image_path, contrast_factor):
    try:
        # Open the image
        image = Image.open(input_image_path)

        # Create an enhancer object for contrast
        enhancer = ImageEnhance.Contrast(image)

        # Modify the contrast using the factor provided
        modified_image = enhancer.enhance(contrast_factor)

        # Save the modified image to the output path
        modified_image.save(output_image_path)

        print("Contrast modification successful!")
    except Exception as e:
        print(f"Error: {e}")


# untested
def modify_color_balance(
    input_image_path, output_image_path, red_factor, green_factor, blue_factor
):
    try:
        # Open the image
        image = Image.open(input_image_path)

        # Split the image into individual channels
        r, g, b = image.split()

        # Modify the intensity of each channel using the provided factors
        r = r.point(lambda i: i * red_factor)
        g = g.point(lambda i: i * green_factor)
        b = b.point(lambda i: i * blue_factor)

        # Merge the modified channels back into a new image
        modified_image = Image.merge("RGB", (r, g, b))

        # Save the modified image to the output path
        modified_image.save(output_image_path)

        print("Color balance modification successful!")
    except Exception as e:
        print(f"Error: {e}")


def modify_saturation(input_image_path, output_image_path, saturation_factor):
    try:
        # Open the image
        image = Image.open(input_image_path)

        # Convert the image to HSL color model
        hsl_image = image.convert("HSV")

        # Split the HSL image into individual channels
        h, s, l = hsl_image.split()

        # Modify the intensity of the saturation channel using the provided factor
        s = s.point(lambda i: i * saturation_factor)

        # Merge the modified channels back into a new HSL image
        modified_hsl_image = Image.merge("HSV", (h, s, l))

        # Convert the modified HSL image back to RGB color model
        modified_image = modified_hsl_image.convert("RGB")

        # Save the modified image to the output path
        modified_image.save(output_image_path)

        print("Saturation modification successful!")
    except Exception as e:
        print(f"Error: {e}")


def modify_sharpness(input_image_path, output_image_path, sharpness_factor):
    try:
        # Open the image
        image = Image.open(input_image_path)

        # Create an enhancer object for sharpness
        enhancer = ImageEnhance.Sharpness(image)

        # Modify the sharpness using the factor provided
        modified_image = enhancer.enhance(sharpness_factor)

        # Save the modified image to the output path
        modified_image.save(output_image_path)

        print("Sharpness modification successful!")
    except Exception as e:
        print(f"Error: {e}")


clear()

total = 10
wing = 10
x = 0

for i in range(total):
    x += 1 / total * 10
    out_path = f"{out_dir}/{i}_{str(x)[:5]}.jpeg"

    modify_sharpness(input_path, out_path, x)
