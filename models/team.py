import logging
import random
import time
import json
from typing import Set
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from .player import Player, generate_players

next_team_id = 0

class Team:
	def __init__(self, name):
		global next_team_id
		self.id: int = next_team_id
		next_team_id += 1
		self.name = name
		self.squad: Set[Player] = set()

	def __repr__(self):
		return self.name

	def register_player(self, player: Player):
		self.squad.add(player)
		player.team = self

	def get_random_player(self):
		return random.choice(self.squad)
