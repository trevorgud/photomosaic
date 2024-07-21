from pathlib import Path
import pickle

from PIL import Image

from config import photoExtension


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


def cropImage(image: Image, newDimensions) -> Image:
    w, h = newDimensions
    return image.crop((0, 0, w, h))


def getPhotoPaths(directory):
    return list(Path(directory).rglob("*" + photoExtension))


def writeAlbumFile(albumMeta, writePath):
    p = pickle.dumps(albumMeta)
    f = open(writePath, "wb")
    f.write(p)


def readAlbumFile(readPath):
    f = open(readPath, "rb")
    p = f.read()
    albumMeta = pickle.loads(p)
    return albumMeta