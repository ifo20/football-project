import random
from typing import Dict, List

from models.competition import Competition
from models.league import League
from models.team import Team
from models.user import User
from data.loaders import load_competitions, load_teams

if __name__ == "__main__":
	print("Welcome to my game! Loading...")
	# 1. load all of the data
	competitions: Dict[str, Competition] = load_competitions()
	teams: Dict[str, Team] = load_teams()
	leagues: Dict[str, League] = {}
	for comp_slug, teams_in_competition in teams.items():
		competition = competitions[comp_slug]
		league = League(competition, teams_in_competition)
		leagues[comp_slug] = league
	# note: each league is loaded with appropriate Teams
	# but each team is empty of players at the moment
	# the idea is to only load them when we need them


	# 2. Get personalised info for the user's character
	username = input("Enter your name:\n")
	user = User(username)
	print(f"Created player! {user} ability: {user.ability}")
	# 3a. TODO give option for user to provide positions that their player can play?
	# 3b. TODO give option for user to provide names of friends who will also be included in their team
	# 4. assign user player to a team
	user_team = random.choice(leagues['national-conference'].teams)
	user_team.register_player(user)
	# 5. introduce their starting variables (salary, abilities..)
	print(f"{user.name} has signed for {user_team.name} on a salary of £{user.salary}/week!")
	# 6. TODO play their first match (are they on the bench?)


