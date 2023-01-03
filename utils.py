import random
import time
from dataclasses import dataclass
from typing import List
from random import *

import os

MODEL = os.environ["MODEL"]


def combine(arr1, arr2, combiner=None):
    combos = []
    for i in arr1:
        for j in arr2:
            if combiner:
                combos.append(combiner(i, j))
            else:
                combos.append((i, j))
    return combos


def random_subset(iter, k):
    shuffled = iter.copy()
    random.shuffle(shuffled)
    return shuffled[:k]


import openai

openai.api_key = "..."

import json


def get_completion(prompt, out=None, verbose=False, as_json=False):
    if verbose:
        print(prompt)
    response = openai.Completion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {
                "role": "assistant",
                "content": "The Los Angeles Dodgers won the World Series in 2020.",
            },
            {"role": "user", "content": "Where was it played?"},
        ],
        temperature=0.7,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    completion = response["choices"][0]["text"].strip()
    if as_json:
        completion = json.loads(completion)
    if verbose:
        print(completion)
    if out:
        print(completion, file=out)
    return completion


def get_chat_completion(prompt, out=None, verbose=False, as_json=False):
    if verbose:
        print(prompt)
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {"role": "user", "content": "%"},
            {
                "role": "assistant",
                "content": "touch my_file.py",
            },
            {
                "role": "user",
                "content": "%",
            },
        ],
    )
    # print(response)
    completion = response["choices"][0]["message"]["content"].strip()
    if as_json:
        completion = json.loads(completion)
    if verbose:
        print(completion)
    if out:
        print(completion, file=out)
    return completion


def get_asst_response(messages):
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
    )
    completion = response["choices"][0]["message"]["content"].strip()
    return completion


@dataclass
class Idea:
    content: str


@dataclass
class IdeaList:
    name: str
    ideas: List[Idea]

    def save(self):
        out = open(f"./lists/{self.name}.txt", "w")
        print(json.dumps([i.content for i in self.ideas]), file=out)

    @staticmethod
    def load(name):
        with open(f"./lists/{name}.txt", "r") as f:
            return IdeaList(name, [Idea(i) for i in json.loads(f.read())])


class Mind:
    def __init__(self, verbose=False) -> None:
        self.verbose = verbose
        pass

    def get_completion(self, prompt):
        return get_completion(prompt, verbose=self.verbose)

    def answer(self, prompt):
        completion = self.get_completion(prompt)
        return completion

    def generate_list(self, list_name, k=10):
        prompt = f"""
            The following is a list of {k} possibilities. These possibilities are not exhaustive and are varied enough that they aren't redundant.
            The name of the list is "{list_name}". This list is structured as an array of strings (without numbers), in JSON format.
        """
        completion = self.get_completion(prompt)
        # Map to Idea objects
        try:
            return IdeaList(list_name, [Idea(c) for c in json.loads(completion)])
        except:
            return None

    def ask_yes_no(self, question):
        prompt = f"""
            {question} Answer "yes" or "no".
        """
        answer = self.get_completion(prompt)
        # Check if answer has correct format
        if "yes" in answer.lower():
            return True
        elif "no" in answer.lower():
            return False
        else:
            raise Exception("Invalid answer")

    def expound(self, idea, context=None):
        prompt = f"""
        Expounded description of the following idea: "{idea}"{ f' as it applies to the subject of "{context}"' if context else ''} - at most 100 words:
        """
        completion = self.get_completion(prompt)
        return completion


import os
import subprocess


def list_files(dir_path):
    # Get list of files in folder
    files = subprocess.check_output(["ls", dir_path]).decode("utf-8")
    return files.split("\n")


def clear_dir(dir_path):
    # Get list of files in folder
    for file in list_files(dir_path):
        if file == "":
            continue
        # Remove file
        os.remove(f"{dir_path}/{file}")


def watch(dir_path, callback):
    # Cached file timestamps
    cached_timestamps = {}
    num_runs = 0
    while True:
        # Get list of files in folder
        files = list_files(dir_path)
        # Check if any files have changed
        for file in files:
            if file == "":
                continue
            # Get file timestamp
            timestamp = os.path.getmtime(f"{dir_path}/{file}")
            # Check if timestamp has changed
            if file not in cached_timestamps:
                if num_runs > 0:
                    callback(file)
                cached_timestamps[file] = timestamp
            elif cached_timestamps[file] != timestamp:
                # File has changed, run code generator
                callback(file)
                cached_timestamps[file] = timestamp
        # Check if any files have been added
        # for file in cached_timestamps:
        #     if file not in files:
        #         callback(file)
        #         del cached_timestamps[file]
        time.sleep(1)
        num_runs += 1
