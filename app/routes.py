from flask import render_template, flash, redirect
from app import app
from fixtures import get_fixture_list, get_teams
from app.forms import LoginForm
from pdb import set_trace


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

    matchdays = get_fixture_list()

    return render_template(
        'index.html',
        title='Home', 
        user=user, 
         teams=[(slug,team["name"]) for slug,team in get_teams().items()],
        matchdays = matchdays,
    )



@app.route('/teams', methods=['GET', 'POST'])
def teams():
    return render_template(
        'teams.html',
        title='Teams', 
        teams=[(slug,team["name"]) for slug,team in get_teams().items()],
    )

@app.route('/team/<team_slug>', methods=['GET', 'POST'])
def team(team_slug):
    teams = get_teams()
    


    return render_template(
        'team.html',
        title='Team', 
        team=teams[team_slug],
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)
    
