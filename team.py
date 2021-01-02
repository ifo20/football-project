import logging
import random
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from player import generate_players

class Team:
	def __init__(self, slug, name):
		self.slug = slug
		self.name = name
		self.players = []

	def __str__(self):
		return self.name

	def load_players(self):
		self.players = generate_players(11)

	def get_random_player(self):
		return random.choice(self.players)

def get_matchup():
	TEAMS = [
		('arsenal', 'Arsenal'),
		('chelsea', 'Chelsea'),
		('liverpool', 'Liverpool'),
		('man_city', 'Man City'),
		('man_utd', 'Man United'),
		('spurs', 'Tottenham Hotspur'),
		('wolves', 'Wolves'),
	]
	# pick home team from first 3
	home_slug_name = random.choice(TEAMS[:3])
	# pick away team from others
	away_slug_name = random.choice(TEAMS[3:])
	return Team(*home_slug_name), Team(*away_slug_name)

if __name__== '__main__':
	team = Team('wolves', 'Wolves')
