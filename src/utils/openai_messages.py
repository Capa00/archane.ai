import base64
import io
from enum import Enum
from typing import List

from PIL import Image

import tiktoken
from tiktoken import Encoding


class ChatMessage:
    class Roles(Enum):
        SYSTEM = "system"
        USER = "user"
        ASSISTANT = "assistant"

    def __init__(self, role: Roles, model: str = "gpt-4o", encoding: Encoding = None):
        self.role = role.value
        self.content = []
        self.encoding = encoding or tiktoken.encoding_for_model(model)
        self.text_tokens = 0
        self.file_tokens = 0

    def add_text(self, text: str):
        self.content.append(
            {
                "type": "text",
                "text": text,
            }
        )
        self.text_tokens += count_tokens(text, self.encoding)

    def add_image_url(self, image_url: str):
        url = f"{image_url}"
        self.content.append(
            {
                "type": "image_url",
                "image_url": {"url": url},
            }
        )
        self.file_tokens += count_tokens(url)

    def add_base64_image(self, base64_image):
        url = f"data:{'image/png'};base64,{base64_image}"
        self.content.append(
            {
                "type": "image_url",
                "image_url": {"url": url},
            }
        )
        self.file_tokens += count_tokens(url)

    def add_pil_image(self, image: Image.Image):
        base64_image = images_to_base64([image])[0]
        return self.add_base64_image(base64_image)

    def get_message(self):
        return {
            "role": self.role,
            "content": self.content,
        }

    def get_num_tokens(self):
        return {
            "text_tokens": self.text_tokens,
            # "file_tokens": self.file_tokens,
            # "total": self.text_tokens + self.file_tokens,
        }

def count_tokens(prompt: str, encoding: Encoding = None, model: str = None):
    if prompt is None:
        return 0
    encoding = encoding or tiktoken.encoding_for_model(model)
    num_tokens = len(encoding.encode(prompt))
    return num_tokens

def images_to_base64(images: List[Image.Image]):
    """
    Converts images to base64 encoded strings.

    This function converts a list of images to a list of base64 encoded strings.
    Each image is converted to a PNG format, encoded to base64, and added to the list.

    Args:
        images (List[Image.Image]): A list of Image objects to be converted.

    Returns:
        List[str]: A list of base64 encoded strings representing each image.

    """
    base64_encoded_images = []
    for image in images:
        buf = io.BytesIO()
        image.save(buf, format="jpeg")
        base64_encoded_images.append(base64.b64encode(buf.getvalue()).decode("utf-8"))

    return base64_encoded_images