import json
from flask import Flask, render_template, request, redirect, flash, url_for, session
from datetime import datetime


POINTS_PER_PLACE = 3


def load_clubs():
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


def add_attending_clubs_to_competitions():
    for competition in competitions:
        competition["attending_clubs"] = {}


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()
add_attending_clubs_to_competitions()


def club_attends(club_name: str, competition):
    return club_name in competition["attending_clubs"].keys()


def club_can_afford(places_required: int, club_name: str):
    club = [c for c in clubs if c['name'] == club_name][0]
    return club['points'] >= places_required * POINTS_PER_PLACE


def club_can_purchase_places(places_required: int, club_name: str, competition):
    if places_required > 12:
        flash('Impossible to book more than 12 places - booking refused!')
        return False
    if not club_can_afford(places_required, club_name):
        flash(f"""your current number of points doesn't allow you to register {places_required} competitors to
            the competition""")
        return False
    if club_attends(club_name, competition):
        purchased_places = competition['attending_clubs'][club_name]
        if purchased_places + places_required > 12:
            flash(f'{club_name} would have more than 12 places - booking refused!')
            return False
        else:
            return True
    else:
        return True


def add_purchased_places(places_required: int, club_name: str, competition):
    if club_attends(club_name, competition):
        competition["attending_clubs"][club_name] += places_required
    else:
        competition["attending_clubs"][club_name] = places_required


def competition_finished(competition):
    competition_date = datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S")
    return competition_date < datetime.today()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/show-summary/', methods=['GET', 'POST'])
def show_summary():
    if request.method == 'GET':
        club_email = session.get('email')
    else:
        club_email = request.form['email']
    club = [club for club in clubs if club['email'] == club_email]
    if not club:
        flash("The email you entered hasn't been found in the clubs email")
        return redirect(url_for('index'))
    else:
        club = club[0]
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>/')
def book(competition, club):
    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = [c for c in competitions if c['name'] == competition][0]
    if competition_finished(found_competition):
        flash('You cannot purchase places for a competition which is already finished')
        session['email'] = found_club['email']
        return redirect(url_for('show_summary'))
    if found_club and found_competition:
        return render_template('booking.html', club=found_club, competition=found_competition)
    else:
        flash("Something went wrong - please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchase-places/', methods=['POST'])
def purchase_places():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    competition_name = competition['name']
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    club_name = club['name']
    places = request.form['places']
    places_required = 0
    if len(places) != 0:
        places_required = int(request.form['places'])
    if places_required <= 0:
        flash("The number of places has to be a positive number and at least 1")
        return redirect(f"/book/{competition_name}/{club_name}/")
    if club_can_purchase_places(places_required, club_name, competition):
        competition['number_of_places'] = competition['number_of_places'] - places_required
        club['points'] = club['points'] - (places_required * POINTS_PER_PLACE)
        add_purchased_places(places_required, club_name, competition)
        flash(f'Great - booking complete! - {places_required} places purchased')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display
@app.route('/public-board/')
def public_board():
    return render_template('public_board.html', clubs=clubs)


@app.route('/logout/')
def logout():
    return redirect(url_for('index'))
