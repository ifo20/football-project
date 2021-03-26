import datetime
import random
from typing import Dict, List

from models.competition import Competition
from models.engine import Engine
from models.league import League
from models.team import Team
from models.user import User

if __name__ == "__main__":
	print("Welcome to my game! Loading...")
	# 1. Get personalised info for the user's character
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

	# 3a. Give option for user to provide position that their player plays in
	available_positions = {'GK', 'CB', 'LB', 'RB', 'CM', 'LM', 'RM', 'ST'}
	while True:
		position = input(f"What position do you play? Please enter one of the following:\n{available_positions}\n").strip().upper()
		if position in available_positions:
			break
		print(f"That wasn't a valid position: Please enter one of {available_positions}")
	user = User(first_name, last_name, dob)
	user.position = position

	# 3b. TODO give option for user to provide names of friends who will also be included in their team

	# 4. create game engine, load teams, leagues, assign user player to a lowly team
	engine = Engine() # this will hold all our data together
	engine.setup(user)

	# 6. TODO What next?
	# Do they make some training choices or go straight into their first match (are they on the bench?)?
	# How does time flow in the game? Week-by-week? Day-by-day?
	engine.run()
