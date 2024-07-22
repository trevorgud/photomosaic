from pathlib import Path
import json
import pickle
import math
import time

import numpy
from PIL import Image

from config import *
from color import *
from generator import generatePhotoMosaic
from index import indexAlbum
from models import PhotoMetadata, AlbumMetadata, toJson
from select import selectClosestPhoto
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


mosaic = generatePhotoMosaic(im, cacheAlbumMeta)
mosaic.show()
