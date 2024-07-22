from PIL import Image

from config import *
from color import photoAvgColor
from select import selectClosestPhoto
from translator import GridTranslator
from utils import correctAspect


# Given a target image and an album of photo metadata, use the album photos
# to generate a photo mosaic of the that target image.
# @param targetImage The target image to genrate, as a PIL image.
# @param albumMeta The album of photos, with metadata, as AlbumMetadata.
# @return The generated photo mosaic as a PIL image.
def generatePhotoMosaic(targetImage, albumMeta):
    gridW, gridH = targetPhotoGrid
    scaleW, scaleH = scaleSize
    targetTranslator = GridTranslator(targetPhotoGrid, targetImage.size)
    canvasTranslator = GridTranslator(targetPhotoGrid, (gridW * scaleW, gridH * scaleH))
    canvas = Image.new(mode="RGB", size=(gridW * scaleW, gridH * scaleH))
    for w in range(gridW):
        for h in range(gridH):
            print("Handling position: ", w, h)
            pixW, pixH = targetTranslator.gridCoordToPixCoord((w, h))
            gridPixW, gridPixH = targetTranslator.pixWH()
            targetCrop = targetImage.crop((pixW, pixH, pixW + gridPixW, pixH + gridPixH))
            color = photoAvgColor(targetCrop)
            closestPhoto = selectClosestPhoto(albumMeta, color)
            photoPath = closestPhoto.path
            sampleIm = Image.open(photoPath)
            cropW, cropH = correctAspect(targetAspect, sampleIm.size)
            sampleIm = sampleIm.crop((0, 0, cropW, cropH))
            sampleIm = sampleIm.resize(scaleSize)

            canvasWH = canvasTranslator.gridCoordToPixCoord((w, h))
            canvas.paste(sampleIm, canvasWH)
    return canvas
