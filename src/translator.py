

class GridTranslator:
    def __init__(self, gridWH, photoWH):
        self.gridWH = gridWH
        self.photoWH = photoWH

    def gridCoordToPixCoord(self, gridCoord):
        gridW, gridH = self.gridWH
        photoW, photoH = self.photoWH
        coordW, coordH = gridCoord
        newW = int((photoW / gridW) * coordW)
        newH = int((photoH / gridH) * coordH)
        return (newW, newH)
    
    def pixWH(self):
        gridW, gridH = self.gridWH
        photoW, photoH = self.photoWH
        pixW = int(photoW / gridW)
        pixH = int(photoH / gridH)
        return (pixW, pixH)
