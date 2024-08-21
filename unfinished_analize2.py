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

def floor_to_closest_datetime(given_datetime, datetime_list):
    filtered_datetimes = [dt for dt in datetime_list if dt <= given_datetime]
    if not filtered_datetimes:
        return None
    closest_datetime = max(filtered_datetimes)
    return closest_datetime

def filter_user(username: str, phone_number: str):
    return (not phone_number) or (phone_number[0] != '+') or (username in ["unknown"])

folder = './messages/'
files = os.listdir(folder)
parser = MessageParser(*[f'{folder}{file}' for file in files])
messages = parser.parse()

earliest_date = messages.earliest_date
latest_date = messages.latest_date
users = messages.users

username2dates2messages = {}
step = timedelta(days=1)
_date = earliest_date
dates = []

while _date <= latest_date:
    dates.append(_date)
    _date += step

for username, phone_number in messages.users:
    if filter_user(username, phone_number):
        continue

    username2dates2messages.update({username: {_date: [] for _date in dates}})

for message in messages:
    message: Message

    if filter_user(message.username, message.phone_number):
        continue
    
    floored_date = floor_to_closest_datetime(message.datetime, dates)
    username2dates2messages[message.username][floored_date].append(message)

shutil.rmtree('message_analysis', ignore_errors=True)
os.makedirs('message_analysis')

# ...
