from quote import QuoteGenerator


class App:
    def __init__(self, topic):
        self.topic = topic
        self.size = (1080, 1350)

    def run(self):
        quote = QuoteGenerator(self.topic, self.size)
        quote.make()


if __name__ == "__main__":
    app = App("Life is short")
    app.run()
