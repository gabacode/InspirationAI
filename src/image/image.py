import gc
import textwrap
from datetime import datetime

import torch
from PIL import Image, ImageDraw, ImageChops, ImageEnhance
from diffusers import StableDiffusionPipeline


class ImageGenerator:
    def __init__(self, prompt: str, size: tuple):
        self.prompt = prompt.strip()
        self.size = size
        self.width, self.height = size

    def prepare(self):
        """
        Prepares the background image
        """
        bg_image = self.generate_image()
        image = Image.open(bg_image)
        image = self.resize_and_crop(image, self.width, self.height)
        image = self.apply_tint(image, (200, 200, 200))
        ImageDraw.Draw(image)
        return image

    @staticmethod
    def resize_and_crop(image, target_width, target_height):
        """
        Resize and crop the image to fit the specified size.
        """
        original_width, original_height = image.size
        ratio = max(target_width / original_width, target_height / original_height)
        new_size = (int(original_width * ratio), int(original_height * ratio))
        image = image.resize(new_size, Image.ANTIALIAS)
        crop_x0 = (new_size[0] - target_width) // 2 if new_size[0] > target_width else 0
        crop_y0 = (new_size[1] - target_height) // 2 if new_size[1] > target_height else 0
        crop_x1 = crop_x0 + target_width if new_size[0] > target_width else new_size[0]
        crop_y1 = crop_y0 + target_height if new_size[1] > target_height else new_size[1]
        return image.crop((crop_x0, crop_y0, crop_x1, crop_y1))

    def generate_image(self) -> str:
        """
        Runs inference to generate an image
        """
        args = {
            "prompt": self.prompt,
            "width": 512,
            "height": 512,
            "negative_prompt": ["text", "bad anatomy", "bad hands", "unrealistic", "bad pose", "bad lighting"],
            "num_inference_steps": 100,
            "guidance_scale": 1,
        }

        pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16,
            use_safetensors=True,
        )

        if torch.cuda.is_available():
            print("Using CUDA")
            pipe = pipe.to("cuda")
            pipe.enable_vae_slicing()
            pipe.enable_xformers_memory_efficient_attention()
        else:
            print("Using CPU")
            pipe.enable_sequential_cpu_offload()

        image = pipe(**args).images[0]

        del pipe
        torch.cuda.empty_cache()
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
