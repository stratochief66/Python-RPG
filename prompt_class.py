__author__ = 'Kyle_Laskowski'

class PromptText(object):

    contents = "First turn, good luck!"

    @staticmethod
    def print_out():
        print PromptText.contents
        PromptText.contents = ""

    @classmethod
    def add_to(cls, text_to_add):
        PromptText.contents += "\n"
        PromptText.contents += str(text_to_add)