# TODO: Many of these imports are probably not needed.
from pathlib import Path
import argparse
import json
import pickle
import math
import time

import numpy
from PIL import Image

from config import *
from color import *
from exclude import loadExclusions
from generator import MosaicGenerator
from index import indexAlbum
from models import PhotoMetadata, AlbumMetadata, toJson
from report import GeneratorReport
from select import PhotoSelector
import select
from translator import GridTranslator
from utils import *


# Parse CLI args.
def getArgs():
    parser = argparse.ArgumentParser(description="Generate a photo mosaic")
    parser.add_argument(
        '--reindex',
        action='store_true',
        help='Reindex the photo instead of using previous cache'
    )
    args = parser.parse_args()
    return args


# Load the args.
args = getArgs()


# Decide whether to index the album or use cached index.
cacheAlbumMeta = None
try:
    cacheAlbumMeta = readAlbumFile("./meta.pickle")
except:
    print("No cache found...")
if args.reindex or cacheAlbumMeta is None:
    albumMeta = indexAlbum(photosDir)
    writeAlbumFile(albumMeta, "./meta.pickle")
    cacheAlbumMeta = albumMeta


# Open and prep target image.
im = Image.open(targetPhoto)
im = prepTargetImage(im, targetAspect)

# Load a map (photo path -> boolean) of photos to exclude.
exclusions = loadExclusions()

# Build and run mosaic generator
photoSelector = PhotoSelector(
    albumMeta = cacheAlbumMeta,
    allowedFunc = select.allowedByDistance(3),
    exclusions = exclusions,
)
report = GeneratorReport(targetPhotoGrid)
generator = MosaicGenerator(photoSelector = photoSelector, report = report)
mosaic = generator.generatePhotoMosaic(im)
writePickled(report, reportPath)


# Display the resulting image (either preview or full mode).
preview = True
if preview:
    previewIm = mosaic.resize(im.size)
    previewIm.show()
else:
    mosaic.show()
