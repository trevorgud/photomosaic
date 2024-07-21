import json


class PhotoMetadata:
    def __init__(self, path, avg_color):
        self.path = str(path)
        self.avg_color = tuple(avg_color)


class AlbumMetadata:
    def __init__(self, photos):
        self.photos = photos


def toJson(albumMeta: AlbumMetadata) -> str:
    return json.dumps(albumMeta, default = lambda o: o.__dict__)
