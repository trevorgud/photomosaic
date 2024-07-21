from pathlib import Path
import json
# from types import SimpleNamespace
import pickle

import numpy
from PIL import Image


class PhotoMetadata:
    def __init__(self, path, avg_color):
        self.path = str(path)
        self.avg_color = tuple(avg_color)

class AlbumMetadata:
    def __init__(self, photos):
        self.photos = photos

def toJson(albumMeta: AlbumMetadata) -> str:
    return json.dumps(albumMeta, default = lambda o: o.__dict__)

# def fromJson(jsonStr: str) -> AlbumMetadata:
#     return json.loads(jsonStr, object_hook=lambda d: SimpleNamespace(**d))


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
    w, h = newDimensions
    return image.crop((0, 0, w, h))


photosDir = "C:\\Users\\trevo\\Downloads\\family-photos-clean"
# Use 3:2 aspect ratio.
targetAspect = 1.5
# Photos outside the aspect tolerance will not be used.
aspectTolerance = 0.05
# Each photo used will be scaled to this size.
scaleSize = (750, 500)
# The number of photos (across width, height) to create the final target photo.
# Because initial test has all photos same dimension, the width and height will be the same.
targetPhotoDimension = (32, 32)
photoExtension = ".jpg"


def getPhotoPaths(directory):
    return list(Path(directory).rglob("*" + photoExtension))


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
# newImg.show()


# Given the album path, create the album index/metadata and return as object.
def indexAlbum(albumDir) -> AlbumMetadata:
    photoPaths = getPhotoPaths(albumDir)
    indices = []
    count = 0
    total = len(photoPaths)
    omitted = 0
    for path in photoPaths:
        im = Image.open(path)
        w, h = im.size
        aspect = w / h
        if abs(aspect - targetAspect) > aspectTolerance:
            omitted += 1
        else:
            # For faster testing, only do 10 at a time for now.
            if count > 10:
                break
            count = count + 1
            print("handling valid photo: ", count)
            meta = PhotoMetadata(path = path, avg_color = photoAvgColor(path))
            indices.append(meta)
    print("Total: ", total)
    print("Omitted: ", omitted)
    return AlbumMetadata(photos = indices)


# def writeAlbumJsonFile(albumMeta, writePath):
#     albumJson = toJson(albumMeta)
#     f = open(writePath, "w")
#     f.write(albumJson)

def writeAlbumFile(albumMeta, writePath):
    p = pickle.dumps(albumMeta)
    f = open(writePath, "wb")
    f.write(p)

def readAlbumFile(readPath):
    f = open(readPath, "rb")
    p = f.read()
    albumMeta = pickle.loads(p)
    return albumMeta


albumMeta = indexAlbum(photosDir)
writeAlbumFile(albumMeta, "./meta.pickle")
rAlbum = readAlbumFile("./meta.pickle")
jsonStr = toJson(rAlbum)
print(rAlbum)
print(jsonStr)

# Indexing photos to later generate a target photo.
# Persistent indexing is for faster lookup, indexing 1000 photos takes a few mins.
# validPhotos = []
# indices = []
# count = 0
# total = len(photoPaths)
# omitted = 0
# for path in photoPaths:
#     im = Image.open(path)
#     w, h = im.size
#     aspect = w / h
#     if abs(aspect - targetAspect) > aspectTolerance:
#         omitted += 1
#     else:
#         # For faster testing, only do 10 at a time for now.
#         if count > 10:
#             break
#         count = count + 1
#         print("handling valid photo: ", count)
#         validPhotos.append(path)
#         meta = PhotoMetadata(path = path, avg_color = photoAvgColor(path))
#         indices.append(meta)

# albumMeta = AlbumMetadata(photos = indices)
# albumJson = toJson(albumMeta)
# print(albumJson)



# print("total: ", total)
# print("omitted: ", omitted)


# Photo album stats and analytics:
# minH = float('inf')
# maxH = 0
# minW = float('inf')
# maxW = 0
# minA = float('inf')
# maxA = 0
# sumW = 0
# sumH = 0
# for each in validPhotos:
#     im = Image.open(each)
#     w, h = im.size
#     aspect = w / h
#     # print(aspect)
#     newW, newH = correctAspect(targetAspect, im.size)
#     # print(newW / newH)
#     if aspect > maxA:
#         maxA = aspect
#     if aspect < minA:
#         minA = aspect
#     sumW = sumW + w
#     sumH = sumH + h
#     if h > maxH:
#         maxH = h
#     if h < minH:
#         minH = h
#     if w > maxW:
#         maxW = w
#     if w < minW:
#         minW = w
# print("Height: ", minH, maxH)
# print("Width: ", minW, maxW)
# print ("Avg Aspect: ", sumW / sumH)
# print ("Aspect: ", minA, maxA)
