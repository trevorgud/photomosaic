from color import colorDist
from models import AlbumMetadata

class PhotoSelector():
    def __init__(self, albumMeta, allowedFunc):
        self.albumMeta = albumMeta
        self.allowedFunc = allowedFunc
        # Store the location of the already used photos as a map from path to list of locations used.
        self.usedMatrix = {}

    def selectClosestAllowedPhoto(self, targetColor, location):
        # Maximum possible euclidean distance between two colors.
        MAX_DIST = 442
        closestPhoto = None
        closestDist = MAX_DIST
        for photo in self.albumMeta.photos:
            # Skip consideration for non-allowed photos (ex: already used)
            usedLocations = self.getUsedLocations(photo)
            if not self.allowedFunc(set(usedLocations), location):
                continue
            dist = colorDist(photo.avg_color, targetColor)
            if (dist < closestDist):
                closestDist = dist
                closestPhoto = photo
        self.usedPhoto(photoMeta = closestPhoto, location = location)
        return closestPhoto

    # Location specified as granular pixel coordinates of the target photo.
    def usedPhoto(self, photoMeta, location):
        self.usedMatrix[photoMeta.path].append(location)

    def getUsedLocations(self, photoMeta):
        if photoMeta.path not in self.usedMatrix:
            self.usedMatrix[photoMeta.path] = []
        return self.usedMatrix[photoMeta.path]


def allowedByAllowDiag(usedLocations, location):
    disallowedOffsets = set([
        (0, 1),
        (-1, 0), (0, 0), (1, 0),  # NOTE: (0, 0) not actually needed because no photo will be selected there yet.
        (0, -1),
    ])
    return allowedByAdjacencyHelper(usedLocations, location, disallowedOffsets)

def allowedByAllowNoTouch(usedLocations, location):
    disallowedOffsets = set([
        (-1, 1), (0, 1), (1, 1),
        (-1, 0), (0, 0), (1, 0), # NOTE: (0, 0) not actually needed because no photo will be selected there yet.
        (-1, -1), (-1, 0), (-1, 1),
    ])
    return allowedByAdjacencyHelper(usedLocations, location, disallowedOffsets)

def allowedByAdjacencyHelper(usedLocations, location, disallowedOffsets):
    disallowedLocations = set()
    # TODO: Mixing of x,y and w,h inconsistencies, maybe shouldn't be doing this. Decide on something consistent.
    xl, yl = location
    for offset in disallowedOffsets:
        xo, yo = offset
        disallowedLocations.add((xl + xo, yl + yo))
    # If any intersection between the set of already used locations and the set of disallowed locations, then
    # we reject the choice of this photo at the given location.
    violations = disallowedLocations.intersection(usedLocations)
    return len(violations) == 0


def allowedByAllowAll(usedLocations, location):
    return True

def allowedByNoDuplicates(usedLocations, location):
    return len(usedLocations) == 0
