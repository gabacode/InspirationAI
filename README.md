# InspirationAI

## AI Inspirational Quotes Generator

This project's goal was to provide a template to share some of the incredible discussions I'm having with an LLM I'm developing for another project (still under NDA, sorry)...

Eventually I thought it would have been more interesting to make it "autonomous", and let it generate its own quotes, and images...

Given that I been feeling unwell during the last few days, this has been the perfect project to spend a few hours on to chill a little bit from work; what best break from work than to work on something else? 😅🤧

## This is useless...why?

Most of posts on social media are just a waste of time, and I'm not talking about the time spent on social media, but the time spent on the content itself. They all seem copies of each others, and they totally lack originality.
Apologies for the harsh words, but I'm sure you know what I'm talking about. Life is too short after all, why not make it more interesting with a pinch of organised chaos?

<img src="./images/demo/life.jpg" width="420" alt="example">

Without stating the obvious any further, let's...

## Get Started

Clone:  
`git clone https://github.com/gabacode/InspirationAI.git`

Requirements:

- [Python3](https://www.python.org/downloads/)
- [venv](https://docs.python.org/3/library/venv.html)
- [make](https://www.gnu.org/software/make/manual/make.html) (or just install the requirements manually)
- An NVIDIA GPU with CUDA support (optional, but recommended)
- Download [llama-2-7b-chat.Q4_K_M.gguf](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf?download=true) and place it inside the folder `./models`

Run the installer:  
`make install`

Run the app:  
`make start`

## How it works?

You may notice the entry point for the app is inside a file named `main.py`:

```python
if __name__ == "__main__":
    app = App("Life is short")
    app.run()
```

Based on the string you pass as a parameter, and instance of llama2 (or other .gguf model of your choice) will come up with an inspirational quote and an image to go with it. The text generation bits leverages Langchain and LlamaCPP, while the graphics are handled to StableDiffusion 1.5 and Pillow. You are free, and welcome to tweak the code to your advantage.

This is a quick overview of the parts of the project's folder structure that are relevant to most needs.

```bash
.
├── models
│   └── llama-2-7b-chat.Q4_K_M.gguf - You must download this file
├── README.md
├── requirements.txt
├── scripts
│   ├── install.sh
│   ├── start.sh
│   └── update.sh
└── src
    ├── footer
    │   └── footer.py
    ├── image
    │   └── image.py
    ├── main.py                     - The app entrypoint
    └── quote
        ├── llm
        │   ├── chains.py           - The chains
        │   ├── llm.py              - The LLM settings
        │   └── prompts.py          - The prompts
        └── quote.py                - The quote generator
```

[More info might be added here in the future]
