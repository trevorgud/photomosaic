from config import exclusionsPath


class Exclusions():
    def __init__(self, mapping):
        self.mapping = mapping

    def get(self, key):
        return self.mapping.get(key)


# Load the exclusions file and return it as a dictionary of photo paths.
# Returns wrapper around dict to ensure only .get exposed.
def loadExclusions():
    with open(exclusionsPath, 'r') as file:
        lines = file.readlines()
    # Remove any trailing newline characters
    lines = [line.strip() for line in lines]
    mapping = {}
    for line in lines:
        mapping[line] = True
    return Exclusions(mapping)
