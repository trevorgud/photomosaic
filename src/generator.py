from PIL import Image
import random

from config import *
from color import photoAvgColor
from opener import imageOpen
from translator import GridTranslator
from utils import correctAspect


class MosaicGenerator():
    def __init__(self, photoSelector, report):
        self.photoSelector = photoSelector
        self.report = report

    def generatePhotoMosaic(self, targetImage):
        gridW, gridH = targetPhotoGrid
        scaleW, scaleH = scaleSize
        targetTranslator = GridTranslator(targetPhotoGrid, targetImage.size)
        canvasTranslator = GridTranslator(targetPhotoGrid, (gridW * scaleW, gridH * scaleH))
        canvas = Image.new(mode=imageMode, size=(gridW * scaleW, gridH * scaleH))

        gridCoords = []
        for w in range(gridW):
            for h in range(gridH):
                gridCoords.append((w, h))
        # Random is best for higher restrictions on photo placement (ex: only single use photo with no reuse)
        # TODO: Make this configurable.
        # random.shuffle(gridCoords)

        for each in gridCoords:
            w, h = each
            print("Selecting mosaic position: ", w, h)
            pixW, pixH = targetTranslator.gridCoordToPixCoord((w, h))
            gridPixW, gridPixH = targetTranslator.pixWH()
            targetCrop = targetImage.crop((pixW, pixH, pixW + gridPixW, pixH + gridPixH))
            color = photoAvgColor(targetCrop)

            closestPhoto = self.photoSelector.selectClosestAllowedPhoto(targetColor = color, location = (w, h))
            self.report.placeAtLocation((w, h), closestPhoto.path)

            photoPath = closestPhoto.path
            sampleIm = imageOpen(photoPath)
            cropW, cropH = correctAspect(targetAspect, sampleIm.size)
            sampleIm = sampleIm.crop((0, 0, cropW, cropH))
            sampleIm = sampleIm.resize(scaleSize)
            canvasWH = canvasTranslator.gridCoordToPixCoord((w, h))
            canvas.paste(sampleIm, canvasWH)

        return canvas
