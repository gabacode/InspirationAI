import gc
import textwrap
from datetime import datetime

import torch
from PIL import Image, ImageDraw, ImageChops, ImageEnhance
from diffusers import DiffusionPipeline


class ImageGenerator:
    def __init__(self, quote: str, size: tuple):
        self.quote = quote
        self.size = size
        self.width, self.height = size

    def prepare(self):
        """
        Prepares the background image
        """
        bg_image = self.generate_image()
        image = Image.open(bg_image).resize((self.width, self.height))
        image = self.apply_tint(image, (200, 200, 200))
        ImageDraw.Draw(image)
        return image

    def generate_image(self) -> str:
        """
        Runs inference to generate an image
        """
        args = {
            "prompt": self.quote,
            "width": (self.width // 8) * 8,
            "height": (self.height // 8) * 8,
            "negative_prompt": ["text", "bad anatomy", "bad hands"],
            "num_inference_steps": 4,
            "guidance_scale": 1,
        }

        pipe = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.float16,
            use_safetensors=True,
        )
        pipe.enable_sequential_cpu_offload()

        pipe.load_lora_weights("latent-consistency/lcm-lora-sdxl", adapter_name="lcm")
        pipe.load_lora_weights("TheLastBen/Papercut_SDXL", weight_name="papercut.safetensors", adapter_name="papercut")
        pipe.set_adapters(["lcm", "papercut"], adapter_weights=[1.0, 0.8])

        image = pipe(**args).images[0]

        del pipe
        gc.collect()

        return self.save_image(image)

    @staticmethod
    def save_image(image):
        image_path = "images/" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".jpg"
        image.save(image_path)
        return image_path

    @staticmethod
    def apply_tint(image, tint_color):
        """
        Applies a tint to the image
        """
        ImageChops.multiply(image, Image.new('RGB', image.size, tint_color))
        return ImageEnhance.Brightness(image).enhance(.6)

    @staticmethod
    def add_quote(image, quote, font, wrap_width=24, line_padding=-10):
        """
        Puts the quote in the centre of the image.
        """
        draw = ImageDraw.Draw(image)
        width, height = image.size

        lines = textwrap.wrap(quote, width=wrap_width)
        text_height_total = sum([draw.textsize(line, font=font)[1] for line in lines]) + line_padding * (len(lines) - 1)
        y = (height - text_height_total) / 2

        for line in lines:
            line_width, line_height = draw.textsize(line, font=font)
            x = (width - line_width) / 2
            draw.text((x, y), line, font=font)
            y += line_height + line_padding
