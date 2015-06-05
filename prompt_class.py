__author__ = 'Kyle_Laskowski'

class PromptText(object):

    def __init__(self):
        self.contents = "Initializing string"

    def print_out(self):
        print self.contents
        self.contents = ""

    def add_to(self, text_to_add):
        self.contents += "\n"
        self.contents += str(text_to_add)

    def __repr__(self):
        return "I am the string used to store the prompt text."