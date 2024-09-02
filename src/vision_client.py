from google.cloud import vision
from google.api_core.client_options import ClientOptions

# Google vision client.
# TODO: Don't hard code credentials.
client_options = ClientOptions(api_key = "")
client = vision.ImageAnnotatorClient(client_options = client_options)
