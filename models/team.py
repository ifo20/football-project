import logging
import random
import time
import json
from typing import Set
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from .player import Player

next_team_id = 0

TEAM_CACHE = {}

class Team:
	def __init__(self, name):
		global next_team_id
		self.id: int = next_team_id
		next_team_id += 1
		self.name = name
		self.league = None
		self.squad: Set[Player] = set()
		

	@classmethod
	def new(cls, name):
		if name in TEAM_CACHE:
			return TEAM_CACHE[name]
		c = cls(name)
		TEAM_CACHE[name] = c
		return c

	def __repr__(self):
		return self.name

	def register_player(self, player: Player):
		self.squad.add(player)
		player.team = self

	def get_random_player(self):
		if not self.squad:
			# last resort: generate player
			player = Player.generate()
			self.register_player(player)
			return player
		return random.choice(tuple(self.squad))

	def get_next_fixture(self):
		for fixture in self.league.fixtures:
			home_team = fixture[0]
			away_team = fixture[1]
			if home_team == self or away_team == self:
				return fixture
