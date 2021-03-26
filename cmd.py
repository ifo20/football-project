import datetime
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
	first_name = input("Enter your first name:\n").title()
	last_name = input("Enter your last name:\n").title()
	while True:
		try:
			birth_year = int(input("Enter your year of birth:\n"))
			assert birth_year > 0
			break
		except:
			print("That wasn't a valid year. Please try again\n")
	while True:
		try:
			birth_month = int(input("Enter your month of birth (as a number between 1 and 12):\n"))
			assert birth_month > 0 and birth_month < 13
			break
		except:
			print("That wasn't a valid month. Please try again\n")
	while True:
		try:
			birth_day = int(input("Enter the day/date of your birth (a number between 1 and 31):\n"))
			dob = datetime.date(birth_year, birth_month, birth_day)
			break
		except Exception as e:
			print("That wasn't a valid date. Please try again\n")
	user = User(first_name, last_name, dob)
	print(f"{user.name} has burst onto the footballing scene at just {user.age} years old!")
	print(f"Here are {user.name}'s skills:\n{user.ability}")
	# 3a. TODO give option for user to provide positions that their player can play
	# 3b. TODO give option for user to provide names of friends who will also be included in their team
	# 4. assign user player to a team
	user_team = random.choice(leagues['national-conference'].teams)
	user_team.register_player(user)
	print(f"{user.name} has signed for {user_team.name} on a salary of £{user.salary}/week!")
	# 6. TODO What next? Do they make some training choices or go straight into their first match (are they on the bench?)?
