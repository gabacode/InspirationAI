import textwrap

from PIL import Image, ImageDraw, ImageChops, ImageEnhance


class ImageGenerator:
    def __init__(self, topic: str, size: tuple):
        self.topic = topic
        self.width, self.height = size

    def prepare(self):
        """
        Prepares the background image
        """
        bg_image = "images/bg0.jpg"
        image = Image.open(bg_image).resize((self.width, self.height))
        image = self.apply_tint(image, (200, 200, 200))
        ImageDraw.Draw(image)
        return image

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
