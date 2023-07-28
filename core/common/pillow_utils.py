from core.common.names import *
import copy


def modify_brightness(image: Image, brightness_factor):
    enhancer = ImageEnhance.Brightness(image)

    modified_image = enhancer.enhance(brightness_factor)

    return modified_image


def modify_contrast(image: Image, contrast_factor):
    enhancer = ImageEnhance.Contrast(image)

    modified_image = enhancer.enhance(contrast_factor)

    return modified_image


def modify_color_balance(image: Image, red_factor, green_factor, blue_factor):
    image = ImageOps.exif_transpose(
        image
    )  # Automatically rotates the image based on EXIF data if available
    if image.mode != "RGB":
        # Convert the image to RGB mode if it's not already in RGB
        image = image.convert("RGB")

    r, g, b = image.split()

    r = r.point(lambda i: i * red_factor)
    g = g.point(lambda i: i * green_factor)
    b = b.point(lambda i: i * blue_factor)

    modified_image = Image.merge("RGB", (r, g, b))

    return modified_image


def modify_saturation(image: Image, saturation_factor):
    image = copy.deepcopy(image)

    hsl_image = image.convert("HSV")

    h, s, l = hsl_image.split()

    s = s.point(lambda i: i * saturation_factor)

    modified_hsl_image = Image.merge("HSV", (h, s, l))

    modified_image = modified_hsl_image.convert("RGB")

    return modified_image


def modify_sharpness(image: Image, sharpness_factor):
    enhancer = ImageEnhance.Sharpness(image)

    modified_image = enhancer.enhance(sharpness_factor)

    return modified_image


def reduce_noise(image: Image, radius):
    modified_image = image.filter(ImageFilter.GaussianBlur(radius))

    return modified_image


def adjust_shadow_highlight(image: Image, shadow_factor, highlight_factor):
    image = copy.deepcopy(image)

    r, g, b = image.split()

    r = ImageOps.autocontrast(r, cutoff=shadow_factor, ignore=None)
    g = ImageOps.autocontrast(g, cutoff=shadow_factor, ignore=None)
    b = ImageOps.autocontrast(b, cutoff=shadow_factor, ignore=None)

    modified_image = Image.merge("RGB", (r, g, b))

    brightness_enhancer = ImageEnhance.Brightness(modified_image)
    modified_image = brightness_enhancer.enhance(highlight_factor)

    return modified_image


def rotate_and_flip_image(image: Image, rotate_angle, flip_x, flip_y):
    image = copy.deepcopy(image)

    rotated_image = image.rotate(rotate_angle)

    if flip_x:
        rotated_image = rotated_image.transpose(Image.FLIP_LEFT_RIGHT)

    if flip_y:
        rotated_image = rotated_image.transpose(Image.FLIP_TOP_BOTTOM)

    return rotated_image
