"""
Represents a single season of a table-based competition
e.g. Championship 20/21
"""

from collections import defaultdict
from itertools import combinations
import logging
import time
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from .match import Match

class League:
	def __init__(self, competition, teams):
		self.competition = competition
		self.teams = teams
		for team in teams:
			team.league = self
		# combinations gives us every possible pairing of teams
		self.fixtures = list(combinations(teams, 2))
		# but it does not give us the reverse fixtures,
		# for example, (team A, team B) AND (team B, team A)
		# so we add those now
		reverse_fixtures = [(b, a) for (a, b) in self.fixtures]
		self.fixtures.extend(reverse_fixtures)
		self.matches = []
		self.top_scorer = None
		print(f"Constructed league for {self.competition} with {len(self.teams)} teams: {self.teams}")

	@property
	def table(self):
		#Need games played, won, draw lost, goals f, goals a, gd, pts
		teams = {team.id:defaultdict(int) for team in self.teams}
		for match in self.matches:
			home_team_row = teams[match.home_team.id]
			away_team_row = teams[match.away_team.id]
			home_team_row["games_played"] += 1
			away_team_row["games_played"] += 1
			home_team_row["goals_for"] += match.home_score
			away_team_row["goals_for"] += match.away_score
			home_team_row["goals_against"] += match.away_score
			away_team_row["goals_against"] += match.home_score
			home_team_row["goal_difference"] += match.home_score - match.away_score
			away_team_row["goal_difference"] += match.away_score - match.home_score

			if match.home_score > match.away_score:
				home_team_row["won"] += 1
				home_team_row["points"] += 3
				away_team_row["lost"] += 1
			elif match.home_score < match.away_score:
				home_team_row["lost"] += 1
				away_team_row["won"] += 1
				away_team_row["points"] += 3
			else:
				away_team_row["draw"] += 1
				away_team_row["points"] += 1
				home_team_row["draw"] += 1
				home_team_row["points"] += 1

		table = []
		# key teams by team id so we can attach name info a few lines below
		teams_by_id = {
			team.id: team
			for team in self.teams
		}
		for team_id, team_stats_dict in teams.items():
			# include name info in the row
			team_stats_dict["id"] = team_id
			team_stats_dict["name"] = teams_by_id[team_id].name
			table.append(team_stats_dict)

		table.sort(key=lambda d: (d["points"], d["goal_difference"]), reverse=True)
		for position,team in enumerate(table,1):
			team["position"] = position


		# we could format this nicely here....we will format outside instead
		return table

	@property
	def scorers(self):
		players_that_scored = []
		for match in self.matches:
			scorers_in_match = match.scorers
			players_that_scored.extend(scorers_in_match)

	def play_matches(self):
		for match in self.fixtures:
			# each "match" is just a tuple of Team instances
			home_team, away_team = match
			match = Match(home_team, away_team)
			match.start()
			self.matches.append(match)

if __name__== '__main__':
	league = League()
	league.play_matches()
	print(league.scorers)
	# print("Finished simulating league, table below:")
	# for position, table_row in enumerate(league.table, start=1):
	# 	print(position, table_row["name"], "Played:", table_row["games_played"], "Points:", table_row["points"])
