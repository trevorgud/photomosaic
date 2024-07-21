# Utility class for translating grid coordinates into pixel coordinates.
# The grid level is the higher level grid that defines how the mosaic will be constructed.
# The pixel level is at the level of individual pixel locations in an image file.
# Ex: for a grid of 8x8 and a photo resolution 750x500 we can translate (1,2)
#   into pixel (93,125). Pixel values are truncated (rounded down) to satisfy integer requirement:
#   (floor(750/8)*1, floor(500/8)*2)
class GridTranslator:
    # Constructor for a new translator
    # @param gridWH A tuple representing (width,height) of the grid.
    # @param photoWH A tuple representing (width,height) of a photo.
    def __init__(self, gridWH, photoWH):
        self.gridWH = gridWH
        self.photoWH = photoWH

    # Convert a grid coordinate into a pixel coordinate.
    # @param gridCoord The tuple of grid (w,h) to convert into pixels.
    # @return The pixel coordinates as a tuple of (w,h)
    def gridCoordToPixCoord(self, gridCoord):
        gridW, gridH = self.gridWH
        photoW, photoH = self.photoWH
        coordW, coordH = gridCoord
        newW = int((photoW / gridW) * coordW)
        newH = int((photoH / gridH) * coordH)
        return (newW, newH)
    
    # Get the pixel width and height of a single square in the grid.
    # For grid 8x8 and photo 750x500 we would receive back (floor(750/8), floor(500/8))
    def pixWH(self):
        gridW, gridH = self.gridWH
        photoW, photoH = self.photoWH
        pixW = int(photoW / gridW)
        pixH = int(photoH / gridH)
        return (pixW, pixH)
