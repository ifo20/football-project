from collections import defaultdict
import requests

from bs4 import BeautifulSoup


def load_football_squads():
	url = "http://www.footballsquads.co.uk/eng/2018-2019/engprem.htm"
	prefix = "http://www.footballsquads.co.uk/eng/2018-2019/"
	r = requests.get(url)
	soup = BeautifulSoup(r.text, features="html.parser")
	main_div = soup.find("div", {"id": "main"})
	team_links = []
	for x in main_div.select("h5 > a"):
		this_team_link = x.get('href')
		team_links.append(prefix + this_team_link)
	teams = [] # list(string)
	players = [] # list (dict)
	for link in team_links:
		r = requests.get(link)
		soup = BeautifulSoup(r.text, features="html.parser")
		main_div = soup.find("div", {"id": "main"})
		team_name = ""
		for possible_team_name_tag in main_div.select("font"):
			possible_team_name = possible_team_name_tag.string
			if possible_team_name and len(possible_team_name) > 2: # ignore blanks etc
				team_name = possible_team_name.replace("\n", "").replace("\r", "") # remove line breaks etc
		header_map = {} # col idx -> header name
		for row_idx, player in enumerate(main_div.select("* > tr")):
			if row_idx == 0: # first tr is actually a header row...
				for i, data in enumerate(player.select("td")):
					if data.string:
						header_map[i] = data.string
			else:
				player_data = {} # attribute -> value
				invalid_row = False
				for i, data in enumerate(player.select("td")):
					if i == 0:
						try:
							player_number = int(data.string)
						except (TypeError, ValueError):
							invalid_row = True
							continue
					if i == 1 and not data.string: # missing player name
						invalid_row = True
						continue
					if header_map.get(i) is not None:
						player_data[header_map[i]] = data.string
				if not invalid_row:
					# ensure all headers present
					for h_idx, header in header_map.items():
						if header not in player_data:
							player_data[header] = None
					player_data['team'] = team_name
					players.append(player_data)
	return teams, players

if __name__ == '__main__':
	teams, players = load_football_squads()
	by_team = defaultdict(set)
	for player in players:
		by_team[player['team']].add(player['Name'])
	for team, players in by_team.items():
		print("{}: {} players: {}\n".format(team, len(players), [p.encode("utf-8") for p in players]))