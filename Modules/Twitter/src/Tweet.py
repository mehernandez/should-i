class Tweet:
    def __init__(self, identifier, text, mood):
        self.identifier = identifier
        self.text = text
        self.mood = mood

    def __str__(self):
        return self.get_url

    def get_url(self):
        return 'https://twitter.com/statuses/' + str(self.identifier)