from langchain.chains import LLMChain
from langchain.llms.base import LLM

from quote.llm import QUOTE_PROMPT, CAPTION_PROMPT


def generate_quote(llm: LLM, topic: str) -> str:
    """
    Generates a quote using the LLM model.
    """
    chain = LLMChain(
        llm=llm,
        prompt=QUOTE_PROMPT
    )
    return chain.run({
        "topic": topic
    }).strip()


def generate_caption(llm: LLM, quote: str) -> str:
    """
    Generates a description of the image using the LLM model.
    """
    chain = LLMChain(
        llm=llm,
        prompt=CAPTION_PROMPT
    )
    return chain.run({
        "quote": quote
    }).strip()
