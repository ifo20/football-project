from .player import Player


class User(Player):
	def __init__(self, first_name, last_name, dob):
		super().__init__(first_name, last_name, dob)
		self.salary = 100 # GBP per week
