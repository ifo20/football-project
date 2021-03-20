import logging
import random
import time
import json
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from player import Player, generate_players

class Team:
	def __init__(self, slug, name, players = None):
		self.slug = slug
		self.name = name
		self.players = [
			Player(player)
			if isinstance(player,str)
			else player
			for player in players
		]


	def __str__(self):
		return self.name

	def load_players(self):
		self.players = generate_players(11)

	def get_random_player(self):
		for player in self.players:
			assert isinstance(player, Player)
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

def get_teams():
	with open('premier_league.json') as teams_json:
		raw_teams = json.load(teams_json)
	#set_trace()

	teams = {}
	for team_name, players in raw_teams.items():
		slug = team_name.lower().replace(" ","-")
		teams[slug] = Team(slug, team_name, players)

	return teams

if __name__== '__main__':
	#team = Team('wolves', 'Wolves')
	x=[]
	for i in range(10000000):
		x.append(i)
	print(x)
	time.sleep(1000)
