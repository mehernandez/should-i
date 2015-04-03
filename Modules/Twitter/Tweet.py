class Tweet:

	def __init__(self, id, text, mood):
		self.id = id		
		self.text = text
		self.mood = mood

	def __str__(self):
		return self.getUrl()

	def getUrl(self):
		return "https://twitter.com/statuses/" + str(self.id)