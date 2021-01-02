import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import random

NULL = "NULL"
ATTACK_START = "ATTACK_START"
THROUGH_BALL = "THROUGH_BALL"
ONE_ON_ONE = "ONE_ON_ONE"
LONG_SHOT = "LONG_SHOT"
GOAL_SCORED = "GOAL_SCORED"
NORMAL_SAVE = "NORMAL_SAVE"
GREAT_SAVE = "GREAT_SAVE"
POST_HIT = "POST_HIT"
SHOT_OVER = "SHOT_OVER"
KICK_OFF = "KICK_OFF"
GOAL_KICK = "GOAL_KICK"
TACKLE = "TACKLE"
DRIBBLE = "DRIBBLE"
BAD_TACKLE = "BAD_TACKLE"
YELLOW_CARD = "YELLOW_CARD"
HANDBALL = "HANDBALL"
FOUL = "FOUL"
FREEKICK = "FREEKICK"

EVENTS = {}

def register(cls):
	EVENTS[cls.KEY] = cls
	return cls

class Event:
	KEY = "TBC" # identifier for this event
	PARAMS = {} # required to describe this event
	PRECEDES = [] # what events can follow this event
	TEXTS = [] # commentary to display
	UPDATES = {} # important changes to update on the Match object

	def __init__(self, **kwargs):
		for k in self.PARAMS:
			assert k in kwargs, "{} was not given param {}".format(self.KEY, k)
		self.params = dict(**kwargs)

	def __str__(self):
		# for example: "ATTACK_START:team=mancity"
		return "{}:{}".format(
			self.KEY,
			",".join((
				"{}={}".format(k, v)
				for k, v in self.params.items()
			)),
		)

	def generate_next(self, **kwargs):
		"""Create the next Event based on self (previous event) + some match kwargs"""
		logger.debug("Generating next event after: %s", self.KEY)
		next_event_key = random.choice(self.PRECEDES)
		logger.debug("Chosen next event KEY: %s", next_event_key)
		match_kwargs = dict(**kwargs)
		# based on this event's params, generate params for next event
		if next_event_key == NULL:
			# forget all previous parameters
			next_event_params = {}
		else: # pass on all params from previous event
			next_event_params = match_kwargs
			next_event_params.update(self.params)
			logger.debug("Remembering previous params from %s for %s: %s", self.KEY, next_event_key, next_event_params)
			next_event_params.update(self.get_next_params(next_event_key, **match_kwargs))
		logger.debug("Got next params for %s: %s", next_event_key, next_event_params)
		next_event_cls = EVENTS[next_event_key]
		next_event_instance = next_event_cls(**next_event_params)
		print(next_event_instance.get_text())
		return next_event_instance

	@classmethod
	def get_params(cls, **kwargs):
		"""Get required event params from match kwargs"""
		return {}

	def get_next_params(self, next_event_key, **kwargs):
		"""Given the event that will follow this (+ match kwargs), get the params for that event"""
		match_kwargs = dict(kwargs)
		return match_kwargs

	def get_text(self):
		if not self.TEXTS:
			return ""
		try:
			return random.choice(self.TEXTS).format(**self.params)
		except KeyError as e:
			logger.error("Event missing param %s: self.params=%s", e, self.params)
			raise e

@register
class NullEvent(Event):
	KEY = NULL
	PRECEDES = [NULL, ATTACK_START]

	def get_next_params(self, next_event_key, **kwargs):
		if next_event_key == ATTACK_START:
			return {
				"team": random.choice([kwargs["home_team"], kwargs["away_team"]]),
				"other_team": random.choice([kwargs["home_team"], kwargs["away_team"]]),
			}
		return {}

@register
class AttackStartEvent(Event):
	KEY = ATTACK_START
	PARAMS = {'team','other_team'}
	PRECEDES = [THROUGH_BALL, LONG_SHOT, DRIBBLE]
	TEXTS = [
		"{team} launches an attack...",
		"{team} are on the attack...",
	]

	def get_next_params(self, next_event_key, **kwargs):
		if next_event_key == LONG_SHOT:
			return {
				"player": self.params["team"].get_random_player(),
			}
		if next_event_key == THROUGH_BALL:
			return {
				"from_player": self.params["team"].get_random_player(),
				"to_player": self.params["team"].get_random_player(),
			}
		if next_event_key == DRIBBLE:
			return{
				"dribbler": self.params["team"].get_random_player(),
				"tackler": self.params["other_team"].get_random_player(),
			}
		return {}

@register
class ThroughBallEvent(Event):
	KEY = THROUGH_BALL
	PARAMS = {'from_player', 'to_player'}
	PRECEDES = [ONE_ON_ONE, BAD_TACKLE]
	TEXTS = [
		"{from_player} plays a through ball to {to_player}...",
	]

	def get_next_params(self, next_event_key, **kwargs):
		if next_event_key == ONE_ON_ONE:
			return {
				"player": self.params["to_player"],
			}
		elif next_event_key == BAD_TACKLE:
			return {
				"Victim": self.params["to_player"],
				"Tackler": self.params["other_team"].get_random_player(),
			}
		return {}


@register
class LongShotEvent(Event):
	KEY = LONG_SHOT
	PARAMS = {'player'}
	PRECEDES = [GOAL_SCORED, GREAT_SAVE, POST_HIT, SHOT_OVER, NORMAL_SAVE]
	TEXTS = [
		"{player} shoots from distance...",
	]

	def get_next_params(self, next_event_key, **kwargs):
		return {
			"goalkeeper": "the goalkeeper",
		}

@register
class OneOnOneEvent(Event):
	KEY = ONE_ON_ONE
	PARAMS = {'player'}
	PRECEDES = [GOAL_SCORED, GREAT_SAVE, POST_HIT, SHOT_OVER,]
	TEXTS = [
		"{player} is one-on-one with the keeper!",
	]

	def get_next_params(self, next_event_key, **kwargs):
		return {
			"goalkeeper": "the goalkeeper",
		}

@register
class BadTackle(Event):
	KEY = BAD_TACKLE
	PARAMS = {'Tackler','Victim'}
	PRECEDES = [FOUL]
	TEXTS = [
		"{Tackler} attempts a poor tackle on {Victim}!",
	]

	def get_next_params(self, next_event_key, **kwargs):
		return {
			"player": self.params["Victim"],
		}

@register
class Handball(Event):
	KEY = HANDBALL
	PARAMS = {'player'}
	PRECEDES = [YELLOW_CARD]
	TEXTS = [
		"It's a handball from {player}!",
	]

@register
class Foul(Event):
	KEY = FOUL
	PARAMS = {'player'}
	PRECEDES = [FREEKICK]
	TEXTS = [
		"It's a foul from {player}!",
	]

@register
class Freekick(Event):
	KEY = FREEKICK
	PARAMS = {'player'}
	PRECEDES = [ATTACK_START, LONG_SHOT, THROUGH_BALL]
	TEXTS = [
		"{player} takes the freekick.",
	]
	def get_next_params(self, next_event_key, **kwargs):
		if next_event_key == THROUGH_BALL:
			return {
				"from_player": self.params["player"],
				"to_player": self.params["team"].get_random_player(),
			}

		return {}


@register
class YellowCard(Event):
	KEY = YELLOW_CARD
	PARAMS = {'player'}
	PRECEDES = [ATTACK_START]
	TEXTS = [
			"{player} has recived a yellow from the referee.",
			"The ref pulls out a yellow for the player",
		]

@register
class ShotOverEvent(Event):
	KEY = SHOT_OVER
	PARAMS = {'player', 'team'}
	PRECEDES = [GOAL_KICK]
	TEXTS = [
		"Over the bar",
	]

	def get_next_params(self, next_event_key, **kwargs):
		home_team = kwargs["home_team"]
		return {
			"team": kwargs["home_team"] if self.params["team"] == kwargs["away_team"] else kwargs["away_team"],
		}

@register
class PostHitEvent(Event):
	KEY = POST_HIT
	PARAMS = {'player'}
	PRECEDES = [GOAL_KICK]
	TEXTS = [
		"{player} hits the post!",
		"Off the post!",
	]

	def get_next_params(self, next_event_key, **kwargs):
		home_team = kwargs["home_team"]
		return {
			"team": kwargs["home_team"] if self.params["team"] == kwargs["away_team"] else kwargs["away_team"],
		}

@register
class NormalSaveEvent(Event):
	KEY = NORMAL_SAVE
	PARAMS = {'player', 'goalkeeper'}
	PRECEDES = [NULL]
	TEXTS = [
		"Easy save for {goalkeeper}",
	]

@register
class GreatSaveEvent(Event):
	KEY = GREAT_SAVE
	PARAMS = {'player', 'goalkeeper'}
	PRECEDES = [NULL]
	TEXTS = [
		"Great save by {goalkeeper}!",
	]

@register
class TackleEvent(Event):
	KEY = TACKLE
	PARAMS = {'tackler','dribbler'}
	PRECEDES = [FOUL, NULL]
	TEXTS = [
		"{dribbler} has been tackled by {tackler}."
	]
	def get_next_params(self, next_event_key, **kwargs):
		if next_event_key == FOUL:
			return {
				"player": self.params["dribbler"],
			}

@register
class DribbleEvent(Event):
	KEY = DRIBBLE
	PARAMS = {'dribbler', 'tackler'}
	PRECEDES = [FOUL, ONE_ON_ONE, TACKLE]
	TEXTS = [
		"{dribbler} takes on {tackler}."
	]

	def get_next_params(self, next_event_key, **kwargs):
		if next_event_key == ONE_ON_ONE:
			return {
				"player": self.params["team"].get_random_player(),
			}
		elif next_event_key == FOUL:
			return {
				"player": self.params["other_team"].get_random_player(),
			}
		return {}


@register
class GoalScoredEvent(Event):
	KEY = GOAL_SCORED
	PARAMS = {'player', 'team'}
	PRECEDES = [KICK_OFF]
	TEXTS = [
		"Goal for {team}!",
		"{player} scores for {team}!",
		"{player} scores!",
	]
	UPDATES = {'goal_scored'}

	def get_next_params(self, next_event_key, **kwargs):
		home_team = kwargs["home_team"]
		return {
			"team": kwargs["home_team"] if self.params["team"] == kwargs["away_team"] else kwargs["away_team"],
		}


@register
class KickOffEvent(Event):
	KEY = KICK_OFF
	PARAMS = {'team'}
	PRECEDES = [NULL]
	TEXTS = [
		"{team} kick off",
	]

@register
class GoalKickEvent(Event):
	KEY = GOAL_KICK
	PARAMS = {'team'}
	PRECEDES = [NULL]
	TEXTS = [
		"Goal kick to {team}",
	]

for key, event in EVENTS.items():
	assert event.PRECEDES, "Event {} does not precede any other event - please add at least one event that may follow {} (else we will get stuck!)".format(key, key)
