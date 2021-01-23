from flask import render_template, flash, redirect, request
from app import app
from fixtures import get_fixtures
from team import get_teams
from app.forms import LoginForm
from pdb import set_trace
import json


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    teams = get_teams()
    matchdays = get_fixtures(teams)


    return render_template(
        'index.html',
        title='Home', 
        user=user, 
        teams=[(slug,team.name) for slug,team in get_teams().items()],
        matchdays = matchdays,
    )



@app.route('/teams', methods=['GET'])
def teams():
    return render_template(
        'teams.html',
        title='Teams', 
        teams=[(slug,team.name) for slug,team in get_teams().items()],
    )

@app.route('/match_maker', methods=['GET'])
def match_maker():
    return render_template(
        'match.html',
        title='Match', 
        teams=[(slug,team.name) for slug,team in get_teams().items()],
    )

@app.route('/season_maker', methods=['GET'])
def season_maker():
    return render_template(
        'season.html',
        title='Season Of Simulation', 
        teams=[(slug,team.name) for slug,team in get_teams().items()],
    )

@app.route('/season_maker', methods=['POST'])
def run_simulation():
   return json.dumps({
       "table": []
   })

@app.route('/team/<team_slug>', methods=['GET', 'POST'])
def team(team_slug):
    teams = get_teams()
    team = teams[team_slug]
    if request.method == 'POST':
        return render_template('game_page.html', team=team)
    return render_template(
        'team.html',
        title='Team', 
        team=team,
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)
    
