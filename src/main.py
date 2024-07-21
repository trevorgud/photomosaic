from pathlib import Path
import json
import pickle
import math
import time

import numpy
from PIL import Image

from config import *
from color import *
from index import indexAlbum
from models import PhotoMetadata, AlbumMetadata, toJson
from translator import GridTranslator
from utils import *


# # Photo operations, using the first image as sample.
# photoPaths = list(Path(photosDir).rglob("*.jpg"))
# photo = photoPaths[0]
# image = Image.open(photo)

# # Average color usage
# avgColor = photoPathAvgColor(photo)
# print(avgColor)

# # Image cropping usage
# dimensions = correctAspect(targetAspect, image.size)
# newImg = cropImage(image, dimensions)
# # newImg.show()


# Given the album path, create the album index/metadata and return as object.
# def indexAlbum(albumDir) -> AlbumMetadata:
#     photoPaths = getPhotoPaths(albumDir)
#     indices = []
#     count = 0
#     total = len(photoPaths)
#     omitted = 0
#     for path in photoPaths:
#         im = Image.open(path)
#         w, h = im.size
#         aspect = w / h
#         if abs(aspect - targetAspect) > aspectTolerance:
#             omitted += 1
#         else:
#             # For faster testing, only do 10 and then stop.
#             # if count > 10:
#             #     break
#             count = count + 1
#             print("handling valid photo: ", count)
#             meta = PhotoMetadata(path = path, avg_color = photoPathAvgColor(path))
#             indices.append(meta)
#     print("Total: ", total)
#     print("Omitted: ", omitted)
#     return AlbumMetadata(photos = indices)


# albumMeta = indexAlbum(photosDir)
# writeAlbumFile(albumMeta, "./meta.pickle")
cacheAlbumMeta = readAlbumFile("./meta.pickle")
jsonStr = toJson(cacheAlbumMeta)
print(cacheAlbumMeta)
print(jsonStr)


def selectClosestPhoto(albumMeta, targetColor):
    closestPhoto = albumMeta.photos[0]
    closestDist = colorDist(closestPhoto.avg_color, targetColor)
    for photo in albumMeta.photos:
        dist = colorDist(photo.avg_color, targetColor)
        if dist < closestDist:
            closestDist = dist
            closestPhoto = photo
    print(targetColor)
    print(closestPhoto.avg_color)
    return closestPhoto


im = Image.open(targetPhoto)
targetWidth, targetHeight = correctAspect(targetAspect, im.size)
im = im.crop((0, 0, targetWidth, targetHeight))
# im.show()

gridW, gridH = targetPhotoGrid
scaleW, scaleH = scaleSize
targetTranslator = GridTranslator(targetPhotoGrid, im.size)
canvasTranslator = GridTranslator(targetPhotoGrid, (gridW * scaleW, gridH * scaleH))

canvas = Image.new(mode="RGB", size=(gridW * scaleW, gridH * scaleH))

for w in range(gridW):
    for h in range(gridH):
        imCopy = im.copy()
        print("Handling position: ", w, h)
        pixW, pixH = targetTranslator.gridCoordToPixCoord((w, h))
        gridPixW, gridPixH = targetTranslator.pixWH()
        print(targetTranslator.gridCoordToPixCoord((w, h)))
        targetCrop = imCopy.crop((pixW, pixH, pixW + gridPixW, pixH + gridPixH))
        color = photoAvgColor(targetCrop)
        # pilShowColor(color)
        # time.sleep(1)
        print(color)
        closestPhoto = selectClosestPhoto(cacheAlbumMeta, color)
        photoPath = closestPhoto.path
        sampleIm = Image.open(photoPath)
        cropW, cropH = correctAspect(targetAspect, sampleIm.size)
        sampleIm = sampleIm.crop((0, 0, cropW, cropH))
        sampleIm = sampleIm.resize(scaleSize)

        canvasWH = canvasTranslator.gridCoordToPixCoord((w, h))
        canvas.paste(sampleIm, canvasWH)

canvas.show()

        # targetCrop.show()


        # canvasPixCoord = canvasTranslator.gridCoordToPixCoord((w, h))
        # pixW0 = w * scaleW
        # pixW1 = pixW0 + scaleW
        # pixH0 = h * scaleH
        # pixH1 = pixH0 + scaleH
        # imSmall = im.crop((pixW0, pixH0, pixW1, pixH1))
        # imSmall.show()
        # break



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
