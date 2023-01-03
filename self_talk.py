from revChatGPT.ChatGPT import Chatbot
import random
from dataclasses import dataclass
from typing import List, Tuple
from utils import combine, get_completion, random_subset
from organons import Organons
import json


def ask_oracle(question):
    prompt = f"""
        I am an intelligent entity with knowledge on a wide variety of topics. I am here to answer your questions.
        I am creative and can think laterally. I answer all questions in 50 words or fewer.
        You've asked me the following question: "{question}".
        My answer is:
    """
    return get_completion(prompt)


def formulate_question(answer, question):
    prompt = f"""
        I am a curious researcher who is looking to learn. I am creative and often think of hypotheticals which may or may not be true.
        I like to think of analogies and metaphors to help me understand things.
        I asked the question: "{question}".
        I got the response: "{answer}".
        I want to focus on a single aspect of that response and ask an unconventional question about it - something that someone wouldn't normally think to ask.
        The question is:
    """
    return get_completion(prompt)


def research(initial_question, depth=1):
    question = initial_question
    for i in range(depth):
        print(f"Q: {question}")
        answer = ask_oracle(question)
        print(f"A: {answer}")
        question = formulate_question(answer, question)


research(
    "What are some ideas around what the Ediacaran fauna were, and how they might be related to living organisms?",
    depth=20,
)
