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
from select import PhotoSelector
import select
from translator import GridTranslator
from utils import *


# albumMeta = indexAlbum(photosDir)
# writeAlbumFile(albumMeta, "./meta.pickle")
cacheAlbumMeta = readAlbumFile("./meta.pickle")
jsonStr = toJson(cacheAlbumMeta)
# print(cacheAlbumMeta)
# print(jsonStr)


im = Image.open(targetPhoto)
im = prepTargetImage(im, targetAspect)


# photoSelector = PhotoSelector(albumMeta = cacheAlbumMeta, allowedFunc = select.allowedByAllowAll)
# TODO: Figure out why no touch selection rule not working, seems to allow adjacent and diagonal.
# photoSelector = PhotoSelector(albumMeta = cacheAlbumMeta, allowedFunc = select.allowedByAllowNoTouch)
photoSelector = PhotoSelector(albumMeta = cacheAlbumMeta, allowedFunc = select.allowedByAllowDiag)
generator = MosaicGenerator(photoSelector = photoSelector)
mosaic = generator.generatePhotoMosaic(im)

preview = True
if preview:
    previewIm = mosaic.resize(im.size)
    previewIm.show()
else:
    mosaic.show()
