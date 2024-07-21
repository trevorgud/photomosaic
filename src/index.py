from PIL import Image

from color import photoPathAvgColor
from config import aspectTolerance, targetAspect
from models import AlbumMetadata, PhotoMetadata
from utils import getPhotoPaths

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
        if (abs(aspect - targetAspect) > aspectTolerance) or (im.mode != "RGB"):
            omitted += 1
        else:
            # For faster testing, only do 10 and then stop.
            # if count > 10:
            #     break
            count = count + 1
            print("handling valid photo: ", count)
            meta = PhotoMetadata(path = path, avg_color = photoPathAvgColor(path))
            indices.append(meta)
    print("Total: ", total)
    print("Omitted: ", omitted)
    return AlbumMetadata(photos = indices)
