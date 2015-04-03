import difflib


class Tweet(object):
    def __init__(self, identifier, text):
        self.identifier = identifier
        self.text = text
        self.url = 'https://twitter.com/statuses/' + str(self.identifier)

    def __str__(self):
        return self.url

    def __repr__(self):
        return self.__dict__

    def __eq__(self, other):
        return (self.identifier == other.identifier) or (difflib.SequenceMatcher(None, self.text, other.text).ratio() > 0.7)