import events
import logging
import time
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from team import get_teams
from fixtures import get_fixtures
from collections import defaultdict

class League:
	def __init__(self):
		self.teams = get_teams()
		self.fixtures = get_fixtures(self.teams)
		self.matches = []

	@property
	def table(self):
		#Need games played, won, draw lost, goals f, goals a, gd, pts
		teams = {k:defaultdict(int) for k in self.teams}
		for match in self.matches:
			home_team_row = teams[match.home_team.slug]
			away_team_row = teams[match.home_team.slug]
			home_team_row["games_played"] += 1
			away_team_row["games_played"] += 1
			home_team_row["goals_for"] += match.home_score
			away_team_row["goals_for"] += match.away_score
			home_team_row["goals_against"] += match.away_score
			away_team_row["goals_against"] += match.home_score
			home_team_row["goal_difference"] += match.home_score - match.away_score
			away_team_row["goal_difference"] += match.home_score - match.away_score

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

		for team in teams:
			table.append(team)

		table.sort()
		return table

	def start(self, tick_period=0):
		logger.info("Kick off! %s vs %s is underway", self.home_team, self.away_team)
		self.events.append((events.KickOffEvent(team=self.home_team), 0))
		while self.minute < 90:
			self.tick()
			time.sleep(tick_period)

		logger.info("The referee blows the final whistle!")
		logger.info("Final score: %s", self.score)

	def tick(self):
		logger.debug("Tick: minute %s event %s", self.minute, self.events[-1])
		self.minute += 1
		print("Minute:", self.minute)
		last_event, last_event_minute = self.events[-1]
		new_event = last_event.generate_next(home_team=self.home_team, away_team=self.away_team)
		if "goal_scored" in new_event.UPDATES:
			logger.debug("goal scored, params=%s", new_event.params)
			if new_event.params["team"] == self.home_team:
				self.home_score += 1
			if new_event.params["team"] == self.away_team:
				self.away_score += 1
			logger.info("%s", self.score)
		self.events.append((new_event, self.minute))

	def get_summary(self):
		# We have stored all events so we can find goals, cards etc
		scorers = []
		for event, minute in self.events:
			if "goal_scored" in event.UPDATES:
				scorers.append("{} '{}".format(event.params["player"], minute))
		print(self.score)
		for scorer in scorers:
			print(scorer)

if __name__== '__main__':
	number_of_games = 5
	# game_speed: 0 is fastest, 0.5-1.0 is relatively normal, 5 is really slow
	game_speed = 0.05
	scores = []
	total_home = 0
	total_away = 0
	for _ in range(number_of_games):
		home_team, away_team = get_matchup()
		home_team.load_players()
		away_team.load_players()
		match = Match(home_team, away_team)
		match.start(game_speed)
		scores.append(match.score)
		total_home += match.home_score
		total_away += match.away_score
		match.get_summary()
	if number_of_games > 1:
		for score in scores:
			print(score)
		logger.info("Average home-away score over %s games: Home %.1f - %.1f Away ", number_of_games, total_home / number_of_games, total_away / number_of_games)