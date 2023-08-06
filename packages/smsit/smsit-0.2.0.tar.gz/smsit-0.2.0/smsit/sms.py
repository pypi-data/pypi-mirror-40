import json
from typing import Union, Generator

ContactList = Union[list, tuple, Generator, str]


class SMS:

    def __init__(self, text: str, receiver: ContactList, sender: str=None):
        self.text = text
        self.receiver = (
            (receiver,)
            if isinstance(receiver, str) else
            tuple(receiver)
        )
        self.sender = sender

    def to_dict(self):
        return {
            'text': self.text,
            'receiver': self.receiver,
            'sender': self.sender
        }

    def __repr__(self):
        return json.dumps(self.to_dict())
