from utils import Mind, get_chat_completion, openai, watch, MODEL
import requests

# from playsound import playsound

# print("hello....")


def get_asst_response(messages):
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
    )
    completion = response["choices"][0]["message"]["content"].strip()
    return completion


# Save messages to file
def save_messages(messages):
    with open("messages.txt", "w") as f:
        for message in messages:
            f.write(f"{message['role']}: {message['content']}")


import json


class Bot:
    def __init__(self, id=-1, prompt="You are a helpful assistant"):
        self.id = id
        self.messages = [
            {
                "role": "system",
                "content": prompt,
            },
        ]
        self.save_messages()

    def ask(self, message):
        self.messages.append(
            {
                "role": "user",
                "content": message,
            }
        )
        res = get_asst_response(self.messages)
        # print("Bot:", res)
        # say(res)
        self.messages.append(
            {
                "role": "assistant",
                "content": res,
            }
        )
        self.save_messages()
        return res

    def save_messages(self):
        with open(f"conversations/{self.id}.json", "w") as f:
            # Save in json format
            json.dump(self.messages, f)

    # Print full conversation
    def print_conversation(self):
        for message in self.messages:
            print(f"{message['role']}: {message['content']}")

    def interact(self):
        # Print the latest message
        print(f"{self.messages[-1]['role']}: {self.messages[-1]['content']}")
        while True:
            user_input = input("You: ")
            if user_input == "exit":
                break
            self.messages.append(
                {
                    "role": "user",
                    "content": user_input,
                }
            )
            res = get_asst_response(self.messages)
            print("Bot:", res)
            # say(res)
            self.messages.append(
                {
                    "role": "assistant",
                    "content": res,
                }
            )
            self.save_messages()

    @classmethod
    def load(cls, id):
        with open(f"conversations/{id}.json", "r") as f:
            messages = json.load(f)
            conversation = cls(id)
            conversation.messages = messages
            return conversation

    # Create or load
    @classmethod
    def get(cls, id):
        try:
            return cls.load(id)
        except FileNotFoundError:
            return cls(id)


eleven_api = "..."


# Make request to elevenlabs API
def say(text):
    url = "https://api.elevenlabs.io/v1/text-to-speech/..."
    headers = {
        "xi-api-key": eleven_api,
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
    }
    data = json.dumps(
        {
            "text": text,
            "voice_settings": {"stability": 1, "similarity_boost": 1},
        }
    )
    response = requests.post(url, headers=headers, data=data)
    # Save response content to mpg4 file
    fp = "./audio/speech.mp3"
    with open(fp, "wb") as f:
        # print("yo!")
        f.write(response.content)
    playsound(fp)
    # print(response.content)


import os

# When a new file appears in the directory, play it with the system's default audio player
# def play_new_files(dir):
#     def cb(latest_file):
#         # print("playering", latest_file)
#         os.system(f"open {dir}/{latest_file}")

#     watch(dir, cb)
#     # # Get list of files in directory
#     # files = os.listdir(dir)
#     # # Get the latest file
#     # latest_file = sorted(files)[-1]
#     # # Play the latest file


def converse(prompt):
    curr = prompt
    messages = [curr]
    bot1 = Bot(
        prompt="You are role-playing as a human named Alice who is on a first date. You always end your answer with a question."
    )
    bot2 = Bot(
        prompt="You are role-playing as a human named Bob who is on a first date. You always end your answer with a question."
    )
    for i in range(4):
        curr = bot1.ask(curr)
        messages.append(curr)
        print("Alice: " + curr)
        curr = bot2.ask(curr)
        messages.append(curr)
        print("Bob: " + curr)
    return messages


def one_off(prompt):
    bot = Bot()
    return bot.ask(prompt)


def summarize(text):
    return one_off(
        'Summarize this conversation in 3 sentences: "'
        + text
        + '". The output should be JSON with format { "summary": ... }'
    )


# Start a chat conversation
def chat():
    bot = Bot()
    bot.interact()
    # convo = converse("How's the weather today?")
    # print(summarize(" ".join(convo)))
    # bot1 = Bot(
    #     prompt="You are role-playing as a human on a first date, and always end your answer with a question. You are interested in getting to know other people and like to ask personal questions."
    # )
    # bot2 = Bot(
    #     prompt="You are role-playing as a human on a first date, and always end your answer with a question. You are interested in getting to know other people and like to ask personal questions."
    # )
    # curr = "Can you tell me an embarassing memory?"
    # while True:
    #     curr = bot1.ask(curr)
    #     print("bot: " + curr)
    #     curr = bot2.ask(curr)
    #     print("human: " + curr)
    # conversation = Conversation.get(2)
    # conversation.interact()
    # print("Welcome to the chatbot!")
    # print("Type 'exit' to exit the chatbot.")
    # messages = [
    #     {
    #         "role": "system",
    #         "content": "You are a helpful assistant",
    #     },
    # ]


#    ç # while True:
#     user_input = input("You: ")
#     if user_input == "exit":
#         break
#     messages.append(
#         {
#             "role": "user",
#             "content": user_input,
#         }
#     )
#     res = get_asst_response(messages)
#     print("Bot:", res)
#     messages.append(
#         {
#             "role": "assistant",
#             "content": res,
#         }
#     )


chat()

# play_new_files("audio")
# get_speech_file("hello")
