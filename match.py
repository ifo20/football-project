import events
import logging
import time
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from team import get_matchup

class Match:
	def __init__(self, home_team, away_team):
		self.home_team = home_team
		self.away_team = away_team
		self.home_score = 0
		self.away_score = 0
		self.minute = 0
		self.events = [] # (event, minute)

	@property
	def score(self):
		return "{} {} - {} {}".format(self.home_team, self.home_score, self.away_score, self.away_team)
		
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