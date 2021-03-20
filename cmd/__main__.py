from typing import List

from models.competition import Competition
from models.player import Player
from models.team import Team
from models.user import User

def load_competitions() -> List[Competition]:
	competitions: List[Competition] = []
	with open('data/competitions.json') as f:
		for competition in f:
			competitions.append(Competition(competition["slug"], competition["name"]))
	return competition

def load_teams() -> List[Team]:
	# TODO load files in data/teams
    pass
	# returned Teams will have players already included

if __name__ == "__main__":
	competitions = load_competitions()
	teams = load_teams()
	# Get personal info
    username = input("Enter your name")
	dob = input("DOB")
	height = input("Height")
	user = User(username, dob, height)
	# Start gameplay (eg assign to random team?)
