from collections import defaultdict
from typing import Dict
import datetime
import random
import time

from data.loaders import load_competitions, load_teams

from .competition import Competition
from .league import League
from .team import Team
from .user import User

class Engine:
	GAME_START_DATE = datetime.datetime(2021, 8, 1, 9) # 9am August 1st

	"""Holds all the game state together & controls time"""
	def __init__(self):
		self.competitions: Dict[str, Competition] = {}
		self.teams: Dict[str, Team] = {}
		self.leagues: Dict[str, League] = {} # competition slug -> League
		self.user: User = None # will be defined in setup()
		self.game_time = self.GAME_START_DATE
		self.active: bool = True # set to False when we want to quit the game

	def setup(self, user: User):
		self.user = user
		self.competitions = load_competitions()
		self.teams = load_teams()
		for comp_slug, teams_in_competition in self.teams.items():
			competition = self.competitions[comp_slug]
			league = League(competition, teams_in_competition)
			self.leagues[comp_slug] = league
		# note: each league is loaded with appropriate Teams
		# but each team is empty of players at the moment
		# the idea is to only load them when we need them

		user_team = random.choice(self.leagues['national-conference'].teams)
		user_team.register_player(user)
		print(f"{user.name} has burst onto the footballing scene at just {user.age} years old!")
		print(f"Here are {user.name}'s skills:\n{user.ability}")
		print(f"{user.name} has signed for {user_team.name} on a salary of £{user.salary}/week!")

	def run(self):
		while self.active:
			self.allow_user_input()
			self.progress()			
		print("Exiting...")

	def progress(self):
		# we will only progress 3 hours at a time
		# nothing will happen between most of these
		# but it means we can always land on 9am or 12pm, 3pm, etc
		self.game_time += datetime.timedelta(hours=3)

	def allow_user_input(self):
		# at various points we want to prompt user for a choice (or many choices)
		if self.game_time.hour < 9: # fast-forward
			return
		print(self.game_time)
		while True:
			# this menu of options should vary depending on whether we are in a matchday or not
			choice = input("What would you like to do?\n[c] Go to the next match\n[x] Some submenu\n[q] Quit\n").strip().lower()
			if choice == 'c':
				fixture = self.user.team.get_next_fixture()
				self.play_match(fixture)
			if choice == 'q':
				self.active = False
				return
			if choice == 'x':
				print("We haven't defined this yet!")
				return
	
	def play_match(self, fixture):
		pass

if __name__ == "__main__":
	engine = Engine()
	engine.load()
