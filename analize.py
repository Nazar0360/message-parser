import matplotlib.pyplot as plt
from message_parser import *
import unicodedata
import shutil
import os
import re

def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    
    Taken from https://github.com/django/django/blob/main/django/utils/text.py
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")

folder = './messages/'
files = os.listdir(folder)
parser = MessageParser(*[f'{folder}{file}' for file in files])
messages = parser.parse()

times = []
for hour in range(24):
    for minute in range(4):
        times.append((hour, minute * 15))

number_of_messages = {}

for message in messages:
    message: Message
    
    if (not message.phone_number) or (message.phone_number[0] != '+') or (message.username == "unknown"):
        continue

    rounded_time = (message.datetime.hour, message.datetime.minute - (message.datetime.minute % 15))
    if (message.username, message.phone_number) not in number_of_messages:
        number_of_messages[(message.username, message.phone_number)] = [0 for _ in times]
    length = len(message.text)
    cap = 3000
    if length > cap:
        # length = cap
        continue
    number_of_messages[(message.username, message.phone_number)][times.index(rounded_time)] += length

shutil.rmtree('message_analysis', ignore_errors=True)
os.makedirs('message_analysis')

for name, phone_number in number_of_messages:
    _times = []
    for hour, minute in times:
        _times.append(f"{hour:02d}:{minute:02d}")
    # times = [f"{hour:02d}:{minute:02d}" for hour, minute in times]
    N = number_of_messages[(name, phone_number)]
    n = sum(N)
    plt.plot(_times, N, label=f"{name} ({n} characters total)")
    plt.xlabel('Time')
    plt.ylabel('Number of characters')
    plt.title('Analysis')
    plt.legend()
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.gcf().set_size_inches(20, 9)
    # plt.show()
    plt.savefig(f'message_analysis/{slugify(name, allow_unicode=True)}_{slugify(phone_number, allow_unicode=True)}.png')
    plt.clf()

# print(number_of_messages)