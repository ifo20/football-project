import csv
import json
import os
from typing import Dict, List

from models.competition import Competition
from models.player import Player
from models.team import Team
from models.user import User

def load_competitions() -> Dict[str, Competition]:
	"""Returns a dictionary of Competitions keyed by slug"""
	competitions: Dict[Competition] = {}
	with open('data/competitions.json') as f:
		json_comps = json.load(f)
		for competition in json_comps:
			slug = competition["slug"]
			name = competition["name"]
			competitions[slug] = Competition(slug, name)
	return competitions

def load_teams() -> Dict[str, Team]:
	"""Return a dictionary of Teams keyed by competition slug. No players are loaded yet"""
	all_teams : Dict[str, Team] = {}
	HOME_TEAM_IDX = 3
	AWAY_TEAM_IDX = 4
	for f in os.listdir('data/teams/'):
		if f.endswith('.csv'):
			comp_teams = set()
			with open(os.path.join('data/teams', f)) as comp_file:
				reader = csv.reader(comp_file, delimiter=',')
				for i, row in enumerate(reader):
					if i == 0:
						continue # skip header row
					comp_teams.add(row[HOME_TEAM_IDX])
					comp_teams.add(row[AWAY_TEAM_IDX])
			comp_slug = f.split('.')[0]
			all_teams[comp_slug] = [
				Team.new(comp_team)
				for comp_team in comp_teams
			]
	return all_teams
