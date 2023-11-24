from PIL import ImageFont, ImageDraw


class Footer:
    def __init__(self, height):
        self.show = False
        self.height = height
        self.trademark = "@gabacode"
        self.font = ImageFont.truetype("fonts/tommy.otf", 52)

    def add(self, im):
        """
        Adds the footer text at the bottom of the image
        """
        if self.show:
            draw = ImageDraw.Draw(im)
            bbox = im.getbbox()
            width = bbox[2]
            text_width, text_height = draw.textsize(self.trademark, font=self.font)
            x = (width - text_width) / 2
            y = self.height - text_height - 20
            draw.text((x, y), self.trademark, font=self.font)
