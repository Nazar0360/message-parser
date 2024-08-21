from dataclasses import dataclass
from datetime import *
from typing import *


@dataclass(frozen=True)
class Message:
    datetime: datetime
    username: str
    phone_number: str
    text: str
    
    MessagePart = Literal["datetime", "username", "phone_number", "message"]

    def __str__(self):
        formatted_date = self.datetime.strftime("%d/%m/%Y %H:%M:%S")
        return f"Message at {formatted_date} by {self.username} ({self.phone_number}): {self.text}"


class Messages(list):
    def __init__(self, messages=None):
        super().__init__()
        self._users = set()
        self._earliest_date = None
        self._latest_date = None
        messages = [] if messages is None else messages

        for message in messages:
            self.append(message)


    # def get_messages(self,
    #                  filter_function: Callable[[Message], bool] = None,
    #                  sort_priority: Sequence[Message.MessagePart] = None,
    #                  reverse=False):
    #     messages = self.copy()
    #     if filter_function is not None:
    #         messages = Messages(filter(filter_function, messages))
    #     if sort_priority is not None:
    #         messages.sort(key=lambda x: [x.__getattribute__(a) for a in sort_priority], reverse=reverse)
    #     return messages

    def append(self, message: Message) -> None:
        super().append(message)
        
        self._users.add((message.username, message.phone_number))

        if self._earliest_date is None:
            self._earliest_date = message.datetime
        else:
            self._earliest_date = min(self._earliest_date, message.datetime)
        
        if self._latest_date is None:
            self._latest_date = message.datetime
        else:
            self._latest_date = max(self._latest_date, message.datetime)
    
    @property
    def users(self):
        return self._users
    
    @property
    def earliest_date(self):
        return self._earliest_date
    
    @property
    def latest_date(self):
        return self._latest_date


class MessageParser:
    @staticmethod
    def __check_date(date: str):
        # date should be in format "dd/mm/yyyy,hh:mm:ss,"
        if len(date) != 20:
            return False
        if date[2] != '/':
            return False
        date = date[:2] + date[3:]
        if date[4] != '/':
            return False
        date = date[:4] + date[5:]
        if date[8] != ',':
            return False
        date = date[:8] + date[9:]
        if date[10] != ':':
            return False
        date = date[:10] + date[11:]
        if date[12] != ':':
            return False
        date = date[:12] + date[13:]
        if date[14] != ',':
            return False
        date = date[:14]
        return all(s.isdigit() for s in date)
    
    @staticmethod
    def __find_message(text: str, starting_index: int = 0):
        start = starting_index
        end = start
        if not MessageParser.__check_date(text[starting_index:starting_index+20]):
            raise ValueError("Starting index should be at the date")
        while True:
            end = text.find('\n', end) + 1
            if end == len(text):
                break
            if MessageParser.__check_date(text[end:end+20]):
                break
        return text[start:end-1], end

    def __init__(self, *files: str):
        self.files = files
    
    def parse(self):
        messages = Messages()
        max_len = max(len(file) for file in self.files)
        for file in self.files:
            print(f'Parsing {file+"... ": <{max_len}}', end='')

            with open(file, 'r', encoding='utf-8') as file:
                text = file.read()
            i = 1 
            while True:
                message, i = MessageParser.__find_message(text, i)
                _date = datetime.strptime(message[:19], '%d/%m/%Y,%H:%M:%S')
                message = message[20:]
                # if username contains a comma, it'll fuck shit up, but I have no idea, how to fix it, so...
                username, phone_number, message = message.split(',', 2)
                msg = Message(_date, username, phone_number, message)
                messages.append(msg)
                
                if i == len(text):
                    break
            
            print('done')
        return messages

if __name__ == '__main__':
    import os
    folder = './messages/'
    files = os.listdir(folder)
    parser = MessageParser(*[f'{folder}{file}' for file in files])
    messages = parser.parse()
    messages = messages.get_messages()[:20]
    for message in messages:
        message: Message
        print(message.datetime, message.username, message.phone_number)
