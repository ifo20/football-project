from .player import Player


class User(Player):
	def __init__(self, name):
		super().__init__(name)
		self.salary = 100 # GBP per week
