from textwrap import dedent

from langchain.prompts import PromptTemplate

QUOTE_PROMPT = PromptTemplate(
    template_format="jinja2",
    input_variables=["topic"],
    template=dedent(
        """
        Use the topic provided to generate an original inspirational quote.
        It should be brief, concise, and easy to understand.
        It has the potential of changing someone's life.
        ---
        Topic: {{ topic }}
        Inspirational Quote:
        """
    ).strip(),
)
