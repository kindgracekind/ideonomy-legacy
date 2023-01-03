from revChatGPT.ChatGPT import Chatbot
import random
from dataclasses import dataclass
from typing import List, Tuple
from utils import combine, get_completion, random_subset
from organons import Organons
import json

pan_divisional_organons = Organons().PAN_DIVISIONAL_ORGANONS


@dataclass
class Idea:
    content: str


# out = open(f"./orgs/{org}.txt", "w")


def ask_yes_no(question):
    prompt = f"""
        {question}? Answer "yes" or "no".
    """
    answer = get_completion(prompt)
    # Check if answer has correct format
    if answer.lower() == "yes":
        return True
    elif answer.lower() == "no":
        return False
    else:
        raise Exception("Invalid answer")


def generate_list(list_name, k):
    prompt = f"""
        The following is a list of {k} possibilities. These possibilities are not exhaustive and are varied enough that they aren't redundant.
        The name of the list is "{list_name}". This list is structued as an array of strings, in JSON format.
    """
    completion = get_completion(prompt)
    try:
        # Map to Idea objects
        return [Idea(c) for c in json.loads(completion)]
    except:
        raise Exception("Completion is not valid JSON")


def select_via_criteria(ilist, criteria, k=1):
    prompt = f"""
        I have the following list: {[i.content for i in ilist]}.
        I want to select the {k} item(s) from that list that best satisfy the criteria: "{criteria}".
        That subset of items is (as a JSON array of strings):
    """
    completion = get_completion(prompt, as_json=True)
    return [Idea(c) for c in completion]


def expound(idea, context=None):
    prompt = f"""
       Expounded description of the following idea: "{idea.content}"{ f' as it applies to the subject of "{context}"' if context else ''} - at most 100 words:
    """
    completion = get_completion(prompt)
    return completion


class ListOrg:
    def __init__(self, name, k=10):
        self.name = name
        print(name)
        self.k = k
        self.generated = None

    def generate(self):
        self.generated = generate_list(self.name, self.k)
        return self.generated

    # Repr for debugging
    def __repr__(self):
        return f"ListOrg({self.name})"

    def save(self, path):
        with open(path, "w") as f:
            f.write(self.name)
            f.write("\n")
            f.write("\n")
            # Write each idea on a new line
            for idea in self.generated:
                f.write(idea.content)
                f.write("\n")


def list_org_generator(str_or_idea):
    # Select random organon
    org = random.choice(pan_divisional_organons)
    # Convert idea to str if necessary
    spark = str_or_idea.content if isinstance(str_or_idea, Idea) else str_or_idea
    templated = org.template(spark)
    return ListOrg(templated, k=5)


def basic_discriminator(list_org, context):
    return select_via_criteria(
        list_org.generated,
        "most surprising or interesting in the context of " + context,
        k=1,
    )


def basic_terminator(ilist):
    return ask_yes_no(f"Does this list contain full sentences? List: '{ilist}'")


# Chain ideas together with a given generator and discriminator
def chain(
    spark, *, generator, discriminator, terminator=None, chain_length=1, context=None
):

    for i in range(chain_length):

        list_org = generator(spark)
        print(f"Chain iteration {i}")

        # Generate list of possibilities
        generated = list_org.generate()
        if terminator:
            halt = terminator(generated)
            if halt:
                return list_org

        # Select one possibility
        spark = discriminator(list_org, context)[0]
    return list_org


res = chain(
    "Ediacaran fauna",
    generator=list_org_generator,
    discriminator=basic_discriminator,
    chain_length=3,
    context="relationship to modern living organisms",
)


print(res.name)
for idea in res.generated:
    print("---")
    print(idea.content)
    print(" ")
    print(expound(idea, res.name))
# # if res:
# #     res.save("./orgs/idea_chain.txt")
