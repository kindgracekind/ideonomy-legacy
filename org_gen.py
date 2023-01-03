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


organons = get_organons()


def template_organons(organons, val):
    return [o.template(val) for o in organons]


orgs = template_organons(organons, "Cooperation")


def generate_organon(org):
    out = open(f"./orgs/{org}.txt", "w")
    prompt = f"""
        The following is a list of 10 possibilities. These possibilities are not exhaustive and are varied enough that they aren't redundant.
        The name of the list is "{org}".
    """
    print("\n", file=out)
    print(org, file=out)
    get_completion(prompt, out=out)


generate_organon(
    "Examples in nature of a smaller or less powerful organism controlling a larger or more powerful organism"
)
