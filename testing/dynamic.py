import colorsys as cs
import numpy as np
from PIL import Image






# Hue is between 0 and 1
# Lightness is 0 to 255
# lightness is 0 to 255


def imageToArray(img):
    """
    This function a loaded PIL image, converts the RGB channels to an array, converts the RGB to HSL, then returns that numpy array
    """
    img = img.convert("HSV")
    data = np.asarray(img).copy()
    # data = np.array([[cs.rgb_to_hsv(pixel[0], pixel[1], pixel[2]) for pixel in column] for column in data])
    return data
def arrayToImage(data):
    """
    This function converts numpy array to an image
    """
    # data = np.array([[cs.hsv_to_rgb(pixel[0], pixel[1], pixel[2]) for pixel in column] for column in data], dtype=np.uint8)
    img = Image.fromarray(data, "HSV")
    img = img.convert("RGB")
    return img

def multiplier(pixel, hueM, satM, valM):
    return [np.uint8(pixel[0] * hueM), np.uint8(pixel[1] * satM), np.uint8(pixel[2] * valM)]
def shift(pixel, hueS, satS, valS):
    return [np.uint8(pixel[0] + hueS), np.uint8(pixel[1] + satS), np.uint8(pixel[2] + valS)]
def transform(transformation, data, hue, sat, val):
    return np.array([[transformation(pixel, hue, sat, val) for pixel in column] for column in data])



# TODO: Load config file

# TODO: Load audio parameterizations from static





# Load image
img = Image.open("testing/test_photo.JPG")
# img = Image.open("testing/HSV_test.PNG") # white, black, red, green, blue, gray



# Indexing array:
# Row, column, HSL channel
data = imageToArray(img)

# This is where we manipulate the data                                                                                WORK HERE

data = transform(multiplier, data, 1, 2, 1)
data = transform(shift, data, 128, 0, 0)








img = arrayToImage(data)
img.save("testing/output.png")
# img.show()