import numpy
from PIL import Image

def colorDist(color1, color2):
    return numpy.linalg.norm(color2 - color1)
    # r1, g1, b1 = color1
    # r2, g2, b2 = color2
    # # Distance formula:
    # # sqrt(delta(r)^2 + delta(g)^2 + delta(b)^2)
    # return math.sqrt(((r2 - r1) ** 2) + ((g2 - g1) ** 2) + ((b2 - b1) ** 2))

def photoPathAvgColor(photoPath):
    image = Image.open(photoPath)
    return photoAvgColor(image)
    # image = Image.open(photoPath)
    # if image.mode == "L":
    #     return None
    # np_image = numpy.array(image)
    # avg_color = numpy.mean(np_image, axis=(0, 1))
    # print(type(avg_color))
    # if isinstance(avg_color, numpy.float64):
    #     for each in np_image:
    #         print(each)
    #     print(photoPath)
    #     image.show()
    #     exit()
    # return avg_color

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

def pilShowColor(color):
    print(type(color))
    print(type(color[0]))
    im = Image.new("RGB", (500, 500), numpyColorToPrimitive(color))
    im.show()
