import logging
import random
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

next_id = 0

class Player:
	def __init__(self, name):
		global next_id
		self.id = next_id
		self.name = name
		next_id += 1

	def __str__(self):
		return self.name

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
