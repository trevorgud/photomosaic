import argparse
import os
import shutil

from config import reportPath
from opener import imageOpen
from utils import readPickled


class GeneratorReport:
    def __init__(self, dimensions):
        w, h = dimensions
        self.dimensions = dimensions
        self.locationMatrix = [[None for _ in range(w)] for _ in range(h)]

    def placeAtLocation(self, loc, path):
        self._validateLocation(loc)
        x, y = loc
        self.locationMatrix[x][y] = path

    def getAtLocation(self, loc):
        self._validateLocation(loc)
        x, y = loc
        return self.locationMatrix[x][y]

    def getCompleteSet(self):
        complete = set()
        for row in self.locationMatrix:
            for photoPath in row:
                complete.add(photoPath)
        return complete

    def _validateLocation(self, loc):
        maxX, maxY = self.dimensions
        x, y = loc
        if x > maxX or y > maxY:
            raise IndexError("placement location index out of range")


# Copy the set of unique photo paths in photoSet into the given directory.
def archivePhotos(photoSet, directory):
    # Check if the destination directory exists; if not, create it
    if not os.path.exists(directory):
        os.makedirs(directory)

    for photoPath in photoSet:
        file_name = os.path.basename(photoPath)
        destination_path = os.path.join(directory, file_name)
        shutil.copy(photoPath, destination_path)


def parse_tuple(s):
    try:
        # Split the input string by comma
        x, y = map(int, s.split(','))
        return (x, y)
    except ValueError:
        raise argparse.ArgumentTypeError("Tuple must be in the format x,y where x and y are integers.")


# Calling this file directly exposes CLI for querying the report after generating mosaic.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""
        Answer questions and perform operations on the generated photomosaic based on reporting/statistics.
        (Currently only locations of used photos)
    """)
    parser.add_argument(
        '--loc',
        type=parse_tuple,
        default=None,
        help='Comma separated tuple, x,y where x is horizontal left right, and y is vertical top to bottom. Ex: 20,31 means 20 across and 31 down.'
    )
    parser.add_argument(
        '--archive',
        type=str,
        default=None,
        help='Path to a directory where photos used in last mosaic will be archived'
    )
    args = parser.parse_args()

    report = readPickled(reportPath)

    if args.loc is not None:
        photoPath = report.getAtLocation(args.loc)
        print(f"Photo at {args.loc}: {photoPath}")
        # Open the photo to confirm you passed the right location:
        im = imageOpen(photoPath)
        im.show()
    elif args.archive is not None:
        archiveDir = args.archive
        usedPhotos = report.getCompleteSet()
        archivePhotos(usedPhotos, archiveDir)
        print(f"Moved {len(usedPhotos)} photos to {archiveDir}")
