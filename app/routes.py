from flask import render_template, flash, redirect, request
from app import app
from app.forms import LoginForm
import json

from models.league import League
from data.loaders import load_competitions, load_teams

def get_teams_by_id():
	# load_teams gives us teams keyed by competition slug, not team slug
	# teams dont even have slugs any more
	# they have an id attribute
	teams = load_teams()
	by_id = {}
	for competition_slug, comp_teams in teams.items():
		for comp_team in comp_teams:
			by_id[comp_team.id] = comp_team
	print(by_id)
	return by_id

def get_team_by_id(team_id):
	return get_teams_by_id()[team_id]


@app.route('/')
@app.route('/index')
def index():
	return render_template(
		'index.html',
		title='Home', 
	)



@app.route('/teams', methods=['GET'])
def teams():
	return render_template(
		'teams.html',
		title='Teams', 
		teams=[(team_id,team.name) for team_id,team in get_teams_by_id().items()],
	)

@app.route('/match_maker', methods=['GET'])
def match_maker():
	return render_template(
		'match.html',
		title='Match', 
		teams=[(team_id,team.name) for team_id,team in get_teams_by_id().items()],
	)

@app.route('/season_maker', methods=['GET'])
def season_maker():
	return render_template(
		'season.html',
		title='Season Of Simulation', 
	)

league = None

@app.route('/season_maker', methods=['POST'])
def run_simulation():
	print(request.values)
	competition_slug = request.values["league"]
	competition = load_competitions()[competition_slug]
	all_teams = load_teams()
	league = League(competition, all_teams[competition_slug])
	league.play_matches()
	print("Finished simulating league, table below:")
	for position, table_row in enumerate(league.table, start=1):
		print(position, table_row["name"], "Played:", table_row["games_played"], "Points:", table_row["points"])
		
	return json.dumps({
		"table": league.table,
		"top_scorer": league.top_scorer,
	})

@app.route('/team/<team_id>', methods=['GET', 'POST'])
def team(team_id):
	this_team = get_team_by_id(int(team_id))
	if request.method == 'POST':
		return render_template('game_page.html', team=this_team)
	return render_template(
		'team.html',
		title='Team', 
		team=this_team,
	)


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for user {}, remember_me={}'.format(
			form.username.data, form.remember_me.data))
		return redirect('/index')
	return render_template('login.html', title='Sign In', form=form)
	
