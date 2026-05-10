from flask import Blueprint, render_template, request, redirect, url_for, jsonify

from flask_login import (
    login_user,
    logout_user,
    login_required
)

from werkzeug.security import check_password_hash

from .models import Institute, Team, Match, Player, User, Sport

main = Blueprint("main", __name__)

@main.route("/")
def home():

    sport_name = request.args.get(
        "sport",
        "Football"
    ).strip()

    sport = Sport.query.filter(
        Sport.name.ilike(sport_name)
    ).first()
    if sport is None:
        sport = Sport.query.order_by(Sport.id.asc()).first()

    institutes = Institute.query.all()
    sports = Sport.query.order_by(Sport.name.asc()).all()

    sport_id = sport.id if sport else None

    if sport_id is None:
        teams = []
        matches = []
        players = []
    else:
        teams = Team.query.filter_by(
            sport_id=sport_id
        ).order_by(
            Team.points.desc()
        ).all()

        matches = Match.query.filter_by(
            sport_id=sport_id
        ).all()

        players = Player.query.join(Team).filter(
            Team.sport_id == sport_id
        ).order_by(
            Player.goals.desc()
        ).limit(5).all()

    return render_template(
        "index.html",

        institutes=institutes,
        teams=teams,
        matches=matches,
        players=players,
        sports=sports,

        sport=sport
    )

@main.route("/api/sport/<sport_name>")
def sport_data(sport_name):

    sport_name = sport_name.strip()

    sport = Sport.query.filter(
        Sport.name.ilike(sport_name)
    ).first()

    if sport is None:
        return jsonify({
            "error": "Sport not found"
        }), 404

    teams = Team.query.filter_by(
        sport_id=sport.id
    ).order_by(
        Team.points.desc()
    ).all()

    matches = Match.query.filter_by(
        sport_id=sport.id
    ).all()

    players = Player.query.join(Team).filter(
        Team.sport_id == sport.id
    ).order_by(
        Player.goals.desc()
    ).limit(5).all()

    return jsonify({

        "teams": [

            {
                "name": team.name,
                "sport": team.sport.name if team.sport else None,
                "institute": team.institute.name if team.institute else None,
                "wins": team.wins,
                "draws": team.draws,
                "losses": team.losses,
                "points": team.points
            }

            for team in teams
        ],

        "matches": [

            {
                "team1": match.team1.name,
                "team2": match.team2.name,
                "score1": match.score1,
                "score2": match.score2,
                "date": match.date
            }

            for match in matches
        ],

        "players": [

            {
                "name": player.name,
                "goals": player.goals,
                "team": player.team.name
            }

            for player in players
        ]
    })

@main.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")

        password = request.form.get("password")

        user = User.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            return redirect(url_for("main.home"))

    return render_template("login.html")

@main.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("main.login"))