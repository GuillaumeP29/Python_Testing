import json
from flask import Flask, render_template, request, redirect, flash, url_for


POINTS_PER_PLACE = 3


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


def addAttendingClubsToCompetitions():
    for competition in competitions:
        competition["attendingClubs"] = {}


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
addAttendingClubsToCompetitions()


def clubAttends(club_name: str, competition):
    return club_name in competition["attendingClubs"].keys()


def clubCanAfford(places_required: int, club_name: str):
    club = [c for c in clubs if c['name'] == club_name][0]
    return club['points'] >= places_required * POINTS_PER_PLACE


def clubCanPurchasePlaces(places_required: int, club_name: str, competition):
    if places_required > 12:
        flash('Impossible to book more than 12 places - booking refused!')
        return False
    if not clubCanAfford(places_required, club_name):
        flash(f"""your current number of points doesn't allow you to register {places_required} competitors to
            the competition""")
        return False
    if clubAttends(club_name, competition):
        purchased_places = competition['attendingClubs'][club_name]
        if purchased_places + places_required > 12:
            flash(f'{club_name} would have more than 12 places - booking refused!')
            return False
        else:
            return True
    else:
        return True


def addPurchasedPlaces(places_required: int, club_name: str, competition):
    if clubAttends(club_name, competition):
        competition["attendingClubs"][club_name] += places_required
    else:
        competition["attendingClubs"][club_name] = places_required


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary/', methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']]
    if not club:
        flash("The email you entered hasen't been found in the clubs email")
        return redirect(url_for('index'))
    else:
        club = club[0]
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>/')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong - please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces/', methods=['POST'])
def purchasePlaces():
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
    if clubCanPurchasePlaces(places_required, club_name, competition):
        competition['numberOfPlaces'] = competition['numberOfPlaces'] - places_required
        club['points'] = club['points'] - (places_required * POINTS_PER_PLACE)
        addPurchasedPlaces(places_required, club_name, competition)
        flash(f'Great - booking complete! - {places_required} places purchased')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display
@app.route('/publicBoard/')
def publicBoard():
    return render_template('public_board.html', clubs=clubs)


@app.route('/logout/')
def logout():
    return redirect(url_for('index'))
