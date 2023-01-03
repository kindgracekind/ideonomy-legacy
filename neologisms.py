from revChatGPT.ChatGPT import Chatbot
import random
from dataclasses import dataclass
from typing import List, Tuple
import re
from utils import combine, get_completion, random_subset


@dataclass
class Prefix:
    content: str
    meanings: List[str]


prog = re.compile(r"\w*\(\d\) (.*)")


def line_to_prefix_definition(s):
    content, rest = s.split(":")
    defs = rest.split(",")
    meanings = []
    for defin in defs:
        result = prog.findall(defin)[0].replace(".", "").strip()
        meanings.append(result)
    return Prefix(content, meanings)


def get_prefixes():
    p = []
    with open("../notes/177 Diverse Prefixes.md") as f:
        lines = f.read().split("\n")
        for line in lines:
            p.append(line_to_prefix_definition(line))
    return p


@dataclass
class Word:
    content: str


def line_to_word(s):
    return Word(s.strip())


def get_words():
    w = []
    with open("../notes/164 Diverse Words.md") as f:
        lines = f.read().split("\n")
        for line in lines:
            w.append(line_to_word(line))
    return w


prefixes = get_prefixes()
words = get_words()

combos = combine(prefixes, words)
pairs = random_subset(combos, 1000)

pairs.sort(key=lambda x: x[0].content)


out = open("neo6.txt", "w")


import time

for prefix, word in pairs:
    neo = (prefix.content + word.content).lower()
    prompt = f"""
     The following is a hypothetical definition for the word: '{neo}'? This word doesn't exist, but its meaning can be determined from its roots.
      The prefix of the word, '{prefix.content}', means '{prefix.meanings[0]}'.
      In addition to the definition, there is an example of how the word might be used in a sentence. 
      This dictionary entry has the format: "<word> (from <prefix> - <meaning of prefix> + <postfix>): <definition>; '<sentence>'".
    """
    get_completion(prompt, out=out)
    time.sleep(1)
