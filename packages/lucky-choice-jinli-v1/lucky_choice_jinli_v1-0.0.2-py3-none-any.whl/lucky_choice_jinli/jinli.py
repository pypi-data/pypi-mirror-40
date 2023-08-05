# coding: utf-8
import random
from hashlib import md5

__all__ = ['Jinli']


class Jinli(object):
    def __init__(self, Jinli_name, choiceList):
        self.jinli_name = Jinli_name
        self.jinli_choice = choiceList

    @property
    def choice(self):
        md_value = md5()
        md_value.update(self.jinli_name.encode("utf-8"))
        random.seed(md_value)
        return random.choice(self.jinli_choice)








