from PIL import Image
import random

from config import *
from color import photoAvgColor
# from select import selectClosestPhoto
from translator import GridTranslator
from utils import correctAspect

# TODO: Turn generator into a class, and inject instance of PhotoSelector (DI).

class MosaicGenerator():
    def __init__(self, photoSelector):
        self.photoSelector = photoSelector

    def generatePhotoMosaic(self, targetImage):
        gridW, gridH = targetPhotoGrid
        scaleW, scaleH = scaleSize
        targetTranslator = GridTranslator(targetPhotoGrid, targetImage.size)
        canvasTranslator = GridTranslator(targetPhotoGrid, (gridW * scaleW, gridH * scaleH))
        canvas = Image.new(mode="RGB", size=(gridW * scaleW, gridH * scaleH))

        gridCoords = []
        for w in range(gridW):
            for h in range(gridH):
                gridCoords.append((w, h))
        # random.shuffle(gridCoords)

        for each in gridCoords:
            w, h = each
            print("Handling position: ", w, h)
            pixW, pixH = targetTranslator.gridCoordToPixCoord((w, h))
            gridPixW, gridPixH = targetTranslator.pixWH()
            targetCrop = targetImage.crop((pixW, pixH, pixW + gridPixW, pixH + gridPixH))
            color = photoAvgColor(targetCrop)
            closestPhoto = self.photoSelector.selectClosestAllowedPhoto(targetColor = color, location = (w, h))
            # Maybe just do this within the select photo func?
            # self.photoSelector.usedPhoto(photo = closestPhoto, location = (w, h))
            photoPath = closestPhoto.path
            sampleIm = Image.open(photoPath)
            cropW, cropH = correctAspect(targetAspect, sampleIm.size)
            sampleIm = sampleIm.crop((0, 0, cropW, cropH))
            sampleIm = sampleIm.resize(scaleSize)
            canvasWH = canvasTranslator.gridCoordToPixCoord((w, h))
            canvas.paste(sampleIm, canvasWH)

        return canvas

# Given a target image and an album of photo metadata, use the album photos
# to generate a photo mosaic of the that target image.
# @param targetImage The target image to genrate, as a PIL image.
# @param albumMeta The album of photos, with metadata, as AlbumMetadata.
# @return The generated photo mosaic as a PIL image.
# def generatePhotoMosaic(targetImage, albumMeta):
#     excludePaths = set()
#     gridW, gridH = targetPhotoGrid
#     scaleW, scaleH = scaleSize
#     targetTranslator = GridTranslator(targetPhotoGrid, targetImage.size)
#     canvasTranslator = GridTranslator(targetPhotoGrid, (gridW * scaleW, gridH * scaleH))
#     canvas = Image.new(mode="RGB", size=(gridW * scaleW, gridH * scaleH))

#     gridCoords = []
#     for w in range(gridW):
#         for h in range(gridH):
#             gridCoords.append((w, h))
#     random.shuffle(gridCoords)

#     for each in gridCoords:
#         w, h = each
#         print("Handling position: ", w, h)
#         pixW, pixH = targetTranslator.gridCoordToPixCoord((w, h))
#         gridPixW, gridPixH = targetTranslator.pixWH()
#         targetCrop = targetImage.crop((pixW, pixH, pixW + gridPixW, pixH + gridPixH))
#         color = photoAvgColor(targetCrop)
#         closestPhoto = selectClosestPhoto(albumMeta = albumMeta, targetColor = color, excludePaths = excludePaths)
#         # Exclude this photo from being used again in another location.
#         excludePaths.add(closestPhoto.path)
#         photoPath = closestPhoto.path
#         sampleIm = Image.open(photoPath)
#         cropW, cropH = correctAspect(targetAspect, sampleIm.size)
#         sampleIm = sampleIm.crop((0, 0, cropW, cropH))
#         sampleIm = sampleIm.resize(scaleSize)
#         canvasWH = canvasTranslator.gridCoordToPixCoord((w, h))
#         canvas.paste(sampleIm, canvasWH)

#     return canvas
