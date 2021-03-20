import logging
import random
from typing import Optional
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from player_ability import PlayerAbility
from team import Team

next_id = 0

class Player:
	def __init__(self, name: str):
		global next_id: int
		self.id: int = next_id
		self.name: str = name
		self.ability: PlayerAbility = PlayerAbility()
		self.team: Optional[Team] = None
		next_id += 1

	def __str__(self):
		return self.name

	def train(self):
		self.ability.train()

def generate_players(number_of_players):
	FIRST_NAME_BANK = ['Ashley', 'Justin', 'Roger', 'Iain', 'Bob', 'Kevin', 'Stuart', 'Dave', 'Diogo', 'Sergio', 'Bruno']
	LAST_NAME_BANK = ['Chai', 'Olliver', 'Smith', 'Jones', 'Cole', 'Keane', 'Wright', 'Yorke', 'Aguero', 'De Bruyne', 'Jota', 'Jimenez', 'Shearer', 'Ferdinand', 'Arteta']
	return [
		Player("{} {}".format(random.choice(FIRST_NAME_BANK), random.choice(LAST_NAME_BANK)))
		for i in range(number_of_players)
	]

if __name__== '__main__':
	player = Player('Ashley Chai')
	player = Player('Ashley Chai')
	player = Player('Ashley Chai')
	player = Player('Ashley Chai')
