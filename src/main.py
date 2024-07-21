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
from select import selectClosestPhoto
from translator import GridTranslator
from utils import *


# albumMeta = indexAlbum(photosDir)
# writeAlbumFile(albumMeta, "./meta.pickle")
cacheAlbumMeta = readAlbumFile("./meta.pickle")
jsonStr = toJson(cacheAlbumMeta)
print(cacheAlbumMeta)
print(jsonStr)


# def selectClosestPhoto(albumMeta, targetColor):
#     closestPhoto = albumMeta.photos[0]
#     closestDist = colorDist(closestPhoto.avg_color, targetColor)
#     for photo in albumMeta.photos:
#         dist = colorDist(photo.avg_color, targetColor)
#         if dist < closestDist:
#             closestDist = dist
#             closestPhoto = photo
#     print(targetColor)
#     print(closestPhoto.avg_color)
#     return closestPhoto


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
