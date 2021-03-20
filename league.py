import events
import logging
import time
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from match import Match
from team import get_teams
from fixtures import get_fixtures
from collections import defaultdict

class League:
	def __init__(self):
		self.teams = get_teams()
		self.fixtures = get_fixtures(self.teams)
		self.matches = []
		self.top_scorer = None

	@property
	def table(self):
		#Need games played, won, draw lost, goals f, goals a, gd, pts
		teams = {k:defaultdict(int) for k in self.teams}
		for match in self.matches:
			home_team_row = teams[match.home_team.slug]
			away_team_row = teams[match.away_team.slug]
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
		for team_slug, team_stats_dict in teams.items():
			# include name info in the row
			team_stats_dict["slug"] = team_slug
			team_stats_dict["name"] = self.teams[team_slug].name
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
		for matchday in self.fixtures:
			# each matchday is a list of "fixture"
			for fixture in matchday:
				# each "fixture" is just a tuple of team "slugs" (not the actual Team class instances)
				home_team_slug, away_team_slug = fixture
				# we want the actual team class
				home_team = self.teams[home_team_slug]
				away_team = self.teams[away_team_slug]
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
