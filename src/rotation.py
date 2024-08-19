import math

from google.cloud import vision
from google.api_core.client_options import ClientOptions
from PIL import Image, ExifTags

from config import photosDir
from utils import getPhotoPaths

# Google vision client.
# TODO: Don't hard code credentials.
options = ClientOptions(api_key = "")
client = vision.ImageAnnotatorClient(client_options = options)


# NOTE: Rotation is extra tricky because of EXIF tags.
# When opening a file, you don't know if its auto correcting for exif or not.
# Won't know if there are many sideways photos until you actually generate photomosaic.
# This is possible solution to that problem.


def hintRotations(photoPaths):
    photoCount = 0
    def printProgress():
        percent = (photoCount / len(photoPaths)) * 100
        percentStr = "{:.1f}".format(percent)
        print(percentStr+"%")

    for path in photoPaths:
        photoCount += 1
        if photoCount % 10 == 0:
            printProgress()

        frot, fmsg = get_image_orientation_from_faces(path)
        erot, emsg = get_image_orientation_from_exif(path)
        if frot != 0 and erot != 0:
            print("May need rotation (both):")
        elif frot != 0:
            print("May need rotation (face):")
        elif erot != 0:
            print("May need rotation (exif):")

        if frot != 0 or erot != 0:
            print(path)
            im = Image.open(path)
            im.show()
            rotationAngle = input("Should I rotate and overwrite? ")
            rotationAngle = int(rotationAngle)
            rotationAngle = rotationAngle * -1
            if rotationAngle != 0:
                rotated = im.rotate(rotationAngle, expand=True)
                exif = get_orientation_cleared_exif(rotated)
                rotated.show()
                confirm = input("ok? ")
                if confirm == "y":
                    rotated.save(path, exif = exif)


def get_image_orientation_from_faces(image_path):
    """Detects faces in an image and returns the rotation angle needed to correct the image."""
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Perform face detection
    response = client.face_detection(image=image)
    faces = response.face_annotations

    if not faces:
        return 0, "No faces detected, cannot determine orientation."

    # Calculate the average roll angle of the detected faces
    avg_roll_angle = sum(face.roll_angle for face in faces) / len(faces)

    # Determine the rotation angle needed to correct the image
    if -45 <= avg_roll_angle <= 45:
        return 0, "Image is correctly oriented."
    elif avg_roll_angle > 45 and avg_roll_angle <= 135:
        return 90, "Image is rotated 90 degrees."
    elif avg_roll_angle < -45 and avg_roll_angle >= -135:
        return -90, "Image is rotated -90 degrees."
    else:
        return 180, "Image is upside down."


def get_image_orientation_from_exif(image_path):
    value = get_exif_orientation_num(image_path)
    if value == 3:
        return 180, "Image is upside down."
    elif value == 6:
        return -90, "Image needs rotation"
    elif value == 8:
        return 90, "Image needs rotation"
    elif value == 5 or value == 7:
        return -1, "Unknown rotation needed (mirroring)"
    return 0, "No relevant exif data found"


def get_exif_orientation_num(image_path):
    try:
        # Open the image file
        image = Image.open(image_path)
        # Get the EXIF metadata
        exif_data = image._getexif()
        # If EXIF data exists
        if exif_data:
            # Find the orientation tag in EXIF data
            for tag, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag, tag)
                if tag_name == 'Orientation':
                    return value
        else:
            return None  # No EXIF data found
    except Exception as e:
        print(f"Error reading EXIF data: {e}")
        return None


def get_orientation_cleared_exif(image):
    # Check if the image has EXIF data
    exif = image.getexif()
    # If EXIF data exists and contains an Orientation tag, correct the orientation
    if exif:
        orientation_key = None
        # Find the orientation key
        for key, value in ExifTags.TAGS.items():
            if value == 'Orientation':
                orientation_key = key
                break
        if orientation_key and orientation_key in exif:
            # Clear the orientation tag
            exif[orientation_key] = 1
    return exif


if __name__ == '__main__':
    photoPaths = getPhotoPaths(photosDir)
    hintRotations(photoPaths)
