from utils import *

my_mind = Mind(verbose=False)


def smash(noun, verb):
    posit = noun.content + " can " + verb.content + "."
    # is_real = my_mind.ask_yes_no(f"Is the following statement true? '{posit}'")
    if not False:
        hypos = my_mind.generate_list(
            "Ways that " + noun.content + " can " + verb.content + "."
        )
        if hypos:
            followup = choice(hypos.ideas)

            cleaned = my_mind.answer(
                'Create a gramatically correct sentence that says "'
                + noun.content
                + " can "
                + verb.content
                + " by "
                + followup.content
                + '".'
            )

            print('DID YOU KNOW: "' + my_mind.expound(cleaned) + '"')

        # good_idea = my_mind.ask_yes_no(
        #     f"Is the following sentence tautological or nonsensical: '{cleaned}'?"
        # )
        # good_idea = my_mind.ask_yes_no(f"Is this a widely believed idea: '{cleaned}'?")


def main():
    # my_mind = Mind(verbose=True)
    my_list = my_mind.generate_list("Things that sleeping bags do")
    for verb, second_verb in zip(my_list.ideas, my_list.ideas[1:]):
        examples = my_mind.generate_list("Things that " + verb.content)
        if examples:
            # for noun in examples.ideas:
            smash(examples.ideas[3], second_verb)
    # # print(my_list)
    # # first, second, *rest = my_list.ideas
    # for idea in examples.ideas:
    #     posit = idea.content + " can " + first.content + "."
    #     is_real = my_mind.ask_yes_no(f"Is the following statement true? '{posit}'")
    #     if not is_real:
    #         hypos = my_mind.generate_list(
    #             "Ways that " + idea.content + " can " + first.content + "."
    #         )

    #         followup = choice(hypos.ideas)

    #         cleaned = my_mind.answer(
    #             'Create a gramatically correct sentence that says "'
    #             + idea.content
    #             + " can "
    #             + first.content
    #             + " by "
    #             + followup.content
    #             + '".'
    #         )

    #         good_idea = my_mind.ask_yes_no(
    #             f"Is the following sentence tautological or nonsensical: '{cleaned}'?"
    #         )
    #         good_idea = my_mind.ask_yes_no(
    #             f"Is this a widely believed idea: '{cleaned}'?"
    #         )
    #         # my_mind.answer(
    #         #     'I have an idea. My idea is this: "'
    #         #     + cleaned
    #         #     + '". I will test this idea by '
    #         # )

    # last_example = examples.ideas[5]
    # ans = my_mind.answer(prompt)
    # print(prompt, ans)
    # for idea in rest:

    # for idea in my_list.ideas:
    #     print(others)
    # print(idea.content)
    # print()
    # my_mind = Mind()
    # output = my_mind.generate_list("Things that flowers do")
    # print(output)
    # output.save()


main()
