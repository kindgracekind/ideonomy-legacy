from utils import *


def main():
    my_mind = Mind()
    output = my_mind.generate_list(
        "Yes or No questions to ask to tell if an idea is interesting or not"
    )
    print(output)
    output.save()


main()
