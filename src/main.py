from PIL import Image
from pathlib import Path

photosDir = "C:\\Users\\trevo\\Downloads\\family-photos"

result = list(Path(photosDir).rglob("*.jpg"))
for each in result:
    print(each)

print("Hello, world!")
