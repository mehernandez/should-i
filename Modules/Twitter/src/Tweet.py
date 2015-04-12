import difflib
import time
from Models.Respuesta import Respuesta


class Tweet(Respuesta):
    def __init__(self, identifier, text, user, date):
        self.identifier = identifier
        self.text = text
        self.url = 'https://twitter.com/statuses/' + str(self.identifier)
        self.username = "@" + user
        date_object = time.strptime(date, "%a %b %d %H:%M:%S +0000 %Y")
        self.date = time.strftime("%B %d, %Y", date_object)

    def __str__(self):
        return self.html

    def __repr__(self):
        return self.__dict__

    def __eq__(self, other):
        return (self.identifier == other.identifier) or (difflib.SequenceMatcher(None, self.text, other.text).ratio() > 0.7)