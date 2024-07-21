from PIL import Image
from pathlib import Path

photosDir = "C:\\Users\\trevo\\Downloads\\family-photos-clean"

photoPaths = list(Path(photosDir).rglob("*.jpg"))

total = len(photoPaths)
omitted = 0

validPhotos = []
for each in photoPaths:
    im = Image.open(each)
    w, h = im.size
    if h > w:
        omitted += 1
    else:
        validPhotos.append(each)

im = Image.open(validPhotos[0])
w, h = im.size
print(w, h)
print("total: ", total)
print("omitted: ", omitted)


print("Hello, world!")
