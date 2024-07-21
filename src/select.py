from color import colorDist
from models import AlbumMetadata


def selectClosestPhoto(albumMeta, targetColor):
    closestPhoto = albumMeta.photos[0]
    closestDist = colorDist(closestPhoto.avg_color, targetColor)
    for photo in albumMeta.photos:
        dist = colorDist(photo.avg_color, targetColor)
        if dist < closestDist:
            closestDist = dist
            closestPhoto = photo
    return closestPhoto
