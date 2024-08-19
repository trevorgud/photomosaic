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

    def _validateLocation(self, loc):
        maxX, maxY = self.dimensions
        x, y = loc
        if x > maxX or y > maxY:
            raise IndexError("placement location index out of range")
