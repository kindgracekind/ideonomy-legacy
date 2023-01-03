from revChatGPT.ChatGPT import Chatbot
import random
from dataclasses import dataclass
from typing import List, Tuple
import re
from utils import combine, get_completion, random_subset


@dataclass
class Organon:
    name: str

    def template(self, val):
        return self.name.replace("<X>", val)


def line_to_organon(s):
    return Organon(s.strip())


def get_organons():
    p = []
    with open("../notes/50 Pan-Divisional Organons.md") as f:
        lines = f.readlines()
        for line in lines:
            p.append(line_to_organon(line))
    return p


class Organons:
    @property
    def PAN_DIVISIONAL_ORGANONS(self):
        return get_organons()
