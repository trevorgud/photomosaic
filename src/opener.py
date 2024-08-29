from PIL import Image

from config import imageMode

def imageOpen(path):
    im = Image.open(path)
    if im.mode != imageMode:
        im = im.convert(imageMode)
    return im
