import datetime
import random
from typing import Optional

from .player_ability import PlayerAbility

next_player_id = 0

class Player:
	def __init__(self, first_name, last_name: str, dob: datetime.date = None):
		global next_player_id
		self.id: int = next_player_id
		next_player_id += 1
		self.first_name = first_name
		self.last_name = last_name
		self.name: str = f"{first_name} {last_name}"
		assert dob is None or isinstance(dob, datetime.date)
		self.dob = dob if dob is not None else datetime.date(random.randint(1990, 2015), random.randint(1, 12), random.randint(1, 28))
		self.ability: PlayerAbility = PlayerAbility()
		self.team = None # updated in team.register_player()

	def __repr__(self):
		return self.name

	@property
	def age(self) -> int:
		"""Returns age in years"""
		return int((datetime.date.today() - self.dob).days // 365.25)

	def train(self):
		self.ability.train()

	def get_injury_duration(self) -> str:
		injury_duration = ["1 game", "2 games", "3 games", "7 games", "1 month", "The rest of the season"]
		player_injury = random.choice(injury_duration)
		print("The player is injured for", player_injury)
		return player_injury

	def player_decision(self, probability: float) -> bool:
		player_said_yes = random.random() < probability
		if player_said_yes:
			print(f'{self.name} said ok.')
			return True
		else:
			print(f'{self.name} said nah i''m good.')
			return False

	@classmethod
	def generate(cls):
		FIRST_NAME_BANK = ['Ashley', 'Justin', 'Roger', 'Iain', 'Bob', 'Kevin', 'Stuart', 'Dave', 'Diogo', 'Sergio', 'Bruno']
		LAST_NAME_BANK = ['Chai', 'Olliver', 'Smith', 'Jones', 'Cole', 'Keane', 'Wright', 'Yorke', 'Aguero', 'De Bruyne', 'Jota', 'Jimenez', 'Shearer', 'Ferdinand', 'Arteta']
		return cls(random.choice(FIRST_NAME_BANK), random.choice(LAST_NAME_BANK))

if __name__== '__main__':
	player = Player("Ashley", "Chai")
	print(player)
	player = Player.generate()
	print(player)
	player = Player.generate()
	print(player)
