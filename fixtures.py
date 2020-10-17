import json
import random
from pdb import set_trace

def generate_all_fixtures_for_season(teams):
	random.shuffle(teams)
	fixtures = [] # (home, away)
	for home_team in teams:
		for away_team in teams:
			if home_team == away_team:
				continue
			fixtures.append((home_team, away_team))
	print("Generated {} fixtures".format(len(fixtures)))
	return fixtures

def teams_can_play(matchday, home, away):
	already_playing = set()
	for scheduled_fixture in matchday:
		existing_home, existing_away = scheduled_fixture
		already_playing.add(existing_home)
		already_playing.add(existing_away)
	# we know who is already scheduled to play on this matchday
	if home in already_playing or away in already_playing:
		return False
	return True

def allocate_fixtures_to_matchdays(fixtures, number_of_matchdays):
	matchdays = [[] for i in range(number_of_matchdays)]
	for fixture in fixtures:
		home_team, away_team = fixture
		for i, matchday in enumerate(matchdays, 1):
			if teams_can_play(matchday, home_team, away_team):
				matchday.append(fixture)
				# print("Scheduled {} vs {} for matchday {}".format(home_team, away_team, i))
				break
	print("Allocated fixtures, opening matchday fixtures below:")
	for f in matchdays[0]:
		print("{} vs {}".format(f[0], f[1]))
	return matchdays

def get_teams():
	with open('premier_league.json') as teams_json:
		raw_teams = json.load(teams_json)
	#set_trace()
	teams = {
		team.lower().replace(" ","-"): {
			"name": team,
			"players": players,
		}
		for team, players in raw_teams.items()
	}
	return teams
	

def get_fixture_list():
	teams = get_teams()
	fixtures = generate_all_fixtures_for_season(list(teams.keys()))
	return allocate_fixtures_to_matchdays(fixtures, (len(teams) - 1)*2)

if __name__ == '__main__':
	get_fixture_list()