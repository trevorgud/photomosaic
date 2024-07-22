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


# Given a target image, prepare it for mosaic and return the prepped image.
def prepTargetImage(targetImage, targetAspect):
    # So far the only thing to do is calculating correct aspect and cropping to that aspect.
    targetWidth, targetHeight = correctAspect(targetAspect, targetImage.size)
    cropped = targetImage.crop((0, 0, targetWidth, targetHeight))
    return cropped


# Crop a given image on the right and bottom sides to match the given dimensions.
# @param image The PIL Image to crop
# @param newDimensions A tuple representing dimensions to crop to.
def cropImage(image: Image, newDimensions) -> Image:
    w, h = newDimensions
    return image.crop((0, 0, w, h))


# The a full list of paths for all files in the given directory (recursively).
def getPhotoPaths(directory):
    return list(Path(directory).rglob("*" + photoExtension))


# Write the album metadata to file at the given path
def writeAlbumFile(albumMeta, writePath):
    p = pickle.dumps(albumMeta)
    f = open(writePath, "wb")
    f.write(p)


# Read album metadata from the given path and return as an AlbumMetadata object.
def readAlbumFile(readPath):
    f = open(readPath, "rb")
    p = f.read()
    albumMeta = pickle.loads(p)
    return albumMeta
