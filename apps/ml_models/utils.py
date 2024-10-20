import base64
from PIL import Image
import io


def base64_to_pil_image(base64_str):
    # if prefix is 'data:image/png;base64,', remove it
    if base64_str.startswith('data:image/png;base64,'):
        base64_str = base64_str.split(',')[1]

    # decode Base64 string to bytes
    image_data = base64.b64decode(base64_str)

    # transform bytes to BytesIO object
    image_bytes = io.BytesIO(image_data)

    # use PIL to open the BytesIO object，return PIL.Image.Image object
    image = Image.open(image_bytes).convert('RGB')

    return image
