from PIL import ImageFont
from langchain.chains import LLMChain

from footer import Footer
from image import ImageGenerator
from quote.llm import load_llm, QUOTE_PROMPT


class QuoteGenerator:
    def __init__(self, topic, size):
        self.llm = load_llm()
        self.width, self.height = size
        self.quote = self.generate_quote(topic)

        self.image = ImageGenerator(topic, size)
        self.footer = Footer(self.height)

    def generate_quote(self, topic: str) -> str:
        """
        Generates a quote using the LLM model.
        """
        chain = LLMChain(
            llm=self.llm,
            prompt=QUOTE_PROMPT
        )
        return chain.run({
            "topic": topic
        })

    def make(self):
        image = self.image.prepare()
        font = ImageFont.truetype("fonts/BebasNeue.otf", 115)

        self.image.add_quote(image, self.quote, font)
        self.footer.add(image)

        image.show()
