import gc

from PIL import ImageFont
from rich import print

from footer import Footer
from image import ImageGenerator
from quote.llm import load_llm, generate_quote, generate_caption


class QuoteGenerator:
    def __init__(self, topic, size):
        self.width, self.height = size
        self.font = ImageFont.truetype("fonts/BebasNeue.otf", 115)
        self.llm = load_llm()
        self.quote = generate_quote(self.llm, topic)
        self.caption = generate_caption(self.llm, self.quote)
        self.unload()

        print({
            "quote": self.quote,
            "caption": self.caption
        })

        self.image = ImageGenerator(self.caption, size)
        self.footer = Footer(self.height)

    def unload(self):
        del self.llm
        gc.collect()

    def make(self):
        image = self.image.prepare()
        self.image.add_quote(image, self.quote, self.font)
        self.footer.add(image)
        image.show()
