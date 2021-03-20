"""
Represents a competition and it's history over many years
"""


class Competition:
	def __init__(self, slug, name):
		self.slug = slug
		self.name = name
		self.history = [] # list of winners

	def __repr__(self):
		return self.name
