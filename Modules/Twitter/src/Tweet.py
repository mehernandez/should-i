class Tweet:
    def __init__(self, identifier, text):
        self.identifier = identifier
        self.text = text
        self.url = 'https://twitter.com/statuses/' + str(self.identifier)

    def __str__(self):
        return self.url

    def __repr__(self):
        return self.__dict__