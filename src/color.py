import numpy
from PIL import Image

# Color utilities
# All colors must be RGB
# Colors are represented as numpy.ndarray, with 3 values for the RGB values.

# Calculate the euclidean distance between one color and another.
# Each color must have type numpy.ndarray
def colorDist(color1, color2):
    return numpy.linalg.norm(color2 - color1)


# Given the path of a photo, calculate the average color for the photo.
def photoPathAvgColor(photoPath):
    image = Image.open(photoPath)
    return photoAvgColor(image)


# Given a PIL Image, calculate the average color for the image.
def photoAvgColor(image):
    # Likely grayscale image, return nothing as all photos must be RGB.
    if image.mode == "L":
        return None
    np_image = numpy.array(image)
    avg_color = numpy.mean(np_image, axis=(0, 1))
    return avg_color


# Convert a numpy ndarray of numpy float64 into tuple of integer.
def numpyColorToPrimitive(color):
    return tuple(int(x) for x in color.tolist())


# "Show" a given color by opening a window displaying only that color.
def pilShowColor(color):
    print(type(color))
    print(type(color[0]))
    im = Image.new("RGB", (500, 500), numpyColorToPrimitive(color))
    im.show()
