# TODO: Many of these imports are probably not needed.
from pathlib import Path
import json
import pickle
import math
import time

import numpy
from PIL import Image

from config import *
from color import *
from generator import MosaicGenerator
from index import indexAlbum
from models import PhotoMetadata, AlbumMetadata, toJson
from report import GeneratorReport
from select import PhotoSelector
import select
from translator import GridTranslator
from utils import *

from vision import get_image_orientation_from_faces


# albumMeta = indexAlbum(photosDir)
# writeAlbumFile(albumMeta, "./meta.pickle")
# cacheAlbumMeta = albumMeta
cacheAlbumMeta = readAlbumFile("./meta.pickle")
# jsonStr = toJson(cacheAlbumMeta)
# print(cacheAlbumMeta)
# print(jsonStr)

im = Image.open(targetPhoto)
im = prepTargetImage(im, targetAspect)


# photoSelector = PhotoSelector(albumMeta = cacheAlbumMeta, allowedFunc = select.allowedByAllowAll)
# photoSelector = PhotoSelector(albumMeta = cacheAlbumMeta, allowedFunc = select.allowedByNoDuplicates)
photoSelector = PhotoSelector(albumMeta = cacheAlbumMeta, allowedFunc = select.allowedByDistance(3))
# TODO: Figure out why no touch selection rule not working, seems to allow adjacent and diagonal.
# photoSelector = PhotoSelector(albumMeta = cacheAlbumMeta, allowedFunc = select.allowedByAllowNoTouch)
# photoSelector = PhotoSelector(albumMeta = cacheAlbumMeta, allowedFunc = select.allowedByAllowDiag)
report = GeneratorReport(targetPhotoGrid)
generator = MosaicGenerator(photoSelector = photoSelector, report = report)
mosaic = generator.generatePhotoMosaic(im)

# Can inspect the report after to see which photo was used in each location.
# print(report.getAtLocation((0, 0)))
# print(report.getAtLocation((18, 13)))

preview = True
if preview:
    previewIm = mosaic.resize(im.size)
    previewIm.show()
else:
    mosaic.show()
