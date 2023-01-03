from revChatGPT.ChatGPT import Chatbot
import random
from dataclasses import dataclass
from typing import List, Tuple
import re
from utils import combine, get_completion, random_subset


@dataclass
class Division:
    name: str
    domain: str


def line_to_division(s):
    domain, name = s.split(" - ")
    return Division(name.strip(), domain.strip())


def get_divisions():
    p = []
    with open("../notes/Divisions of Ideonomy.md") as f:
        lines = f.read().split("\n")
        for line in lines:
            p.append(line_to_division(line))
    return p


out = open("division_selection.txt", "w")

divisions = get_divisions()

# Sort the divisions by name
divisions.sort(key=lambda x: x.name)

divs = "\n- ".join(f"{d.name} - study of {d.domain}" for d in divisions)


prompt = f"""
I'm trying to study the Control Problem in AI. That is, the problem of making sure a superintelligence is aligned with human values.
I'm considering the following divisions of study:
{divs}

Of these, which five would be the most useful and immediately actionable to study, and why?
"""
print(prompt)
get_completion(prompt, out=out)
