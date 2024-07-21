
from color import photoPathAvgColor, pilShowColor
from PIL import Image
import time
from utils import *
from config import *

pathGray = "C:\\Users\\trevo\\Downloads\\family-photos-clean\\2001 Cameroon\\2021-04-30-18-59-0019.jpg"
pathColor = "C:\\Users\\trevo\\Downloads\\family-photos-clean\\2001 Cameroon\\2021-04-30-18-59-0018.jpg"

# color = photoPathAvgColor(pathColor)
# pilShowColor(color)
# time.sleep(1)
# im = Image.open(pathColor)
# im.show()

photoPaths = getPhotoPaths(photosDir)
for path in photoPaths:
    color = photoPathAvgColor(path)
    pilShowColor(color)
    time.sleep(0.1)

    im = Image.open(path)
    im.show()
    print(path)
    print(im.mode)
    print(im.size)
    print(color)
    time.sleep(1)


# im = Image.open(pathGray)
# print(im.get_format_mimetype())
# print(im.mode)
# print(im.format)
# color = photoPathAvgColor(path)
