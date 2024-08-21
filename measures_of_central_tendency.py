from message_parser import *
import os

folder = './messages/'
files = os.listdir(folder)
parser = MessageParser(*[f'{folder}{file}' for file in files])
messages = parser.parse()

lengths = []

for message in messages:
    message: Message
    lengths.append(len(message.text))

number_of_messages = len(lengths)
if number_of_messages == 0:
    print("No messages found.")
    exit()

average_length = sum(lengths) / number_of_messages

lengths.sort()
if number_of_messages % 2 == 0:
    median_length = (lengths[number_of_messages // 2] + lengths[number_of_messages // 2 + 1]) / 2
else:
    median_length = lengths[number_of_messages // 2]

mode_length = max(set(lengths), key=lengths.count)

print(f"\nNumber of messages: {number_of_messages}")
print(f"Average length: {average_length:.2f}")
print(f"Median length: {median_length}")
print(f"Mode length: {mode_length}")
