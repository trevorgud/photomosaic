from PIL import Image
from pathlib import Path
import numpy


class PhotoColor:
    def __init__(self, path, avg_color):
        self.path = path
        self.avg_color = avg_color

class AlbumMetadata:
    def __init__(self, indices):
        self.indices = indices


# Take a target aspect as float and dimensions as tuple (w, h)
# Return a new tuple of dimensions corrected to the target aspect.
def correctAspect(targetAspect, dimensions):
    w, h = dimensions
    currentAspect = w / h
    # General equation: w / h = aspect
    # Calculate the new correct dimension for either width or height.
    if currentAspect > targetAspect:
        # Current width too large, must calculate new width to match height.
        newW = h * targetAspect
        return (int(newW), h)
    else:
        # Current height too large, must calculate new height to match width.
        newH = w / targetAspect
        return (w, int(newH))


def photoAvgColor(photoPath):
    im = Image.open(photoPath)
    np_image = numpy.array(image)
    avg_color = numpy.mean(np_image, axis=(0, 1))
    return avg_color


def cropImage(image: Image, newDimensions) -> Image:
    # only crop from the right and bottom.
    # w, h = image.size
    w, h = newDimensions
    return image.crop((0, 0, w, h))



photosDir = "C:\\Users\\trevo\\Downloads\\family-photos-clean"
targetAspect = 1.5

# Photo operations, using the first image as sample.
photoPaths = list(Path(photosDir).rglob("*.jpg"))
photo = photoPaths[0]
image = Image.open(photo)

# Average color usage
avgColor = photoAvgColor(photo)
print(avgColor)

# Image cropping usage
dimensions = correctAspect(targetAspect, image.size)
newImg = cropImage(image, dimensions)
newImg.show()


total = len(photoPaths)
omitted = 0

validPhotos = []
for each in photoPaths:
    im = Image.open(each)
    w, h = im.size
    if h > w:
        omitted += 1
    else:
        validPhotos.append(each)

print("total: ", total)
print("omitted: ", omitted)

# minH = float('inf')
# maxH = 0
# minW = float('inf')
# maxW = 0
minA = float('inf')
maxA = 0
sumW = 0
sumH = 0
for each in validPhotos:
    im = Image.open(each)
    w, h = im.size
    aspect = w / h
    print(aspect)
    newW, newH = correctAspect(targetAspect, im.size)
    print(newW / newH)
    if aspect > maxA:
        maxA = aspect
    if aspect < minA:
        minA = aspect
    sumW = sumW + w
    sumH = sumH + h
    # if h > maxH:
    #     maxH = h
    # if h < minH:
    #     minH = h
# print("Height: ", minH, maxH)
# print("Width: ", minW, maxW)
print ("Avg Aspect: ", sumW / sumH)
print ("Aspect: ", minA, maxA)


print("Hello, world!")
