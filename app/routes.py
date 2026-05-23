from flask import Blueprint, render_template, request, redirect, url_for, jsonify

from flask_login import (
    login_user,
    logout_user,
    login_required
)

from werkzeug.security import check_password_hash

from sqlalchemy.orm import joinedload

from .models import Team, Match, Player, User, Tournament

main = Blueprint("main", __name__)

@main.route("/")
def home():
    tournaments = Tournament.query.options(
        joinedload(Tournament.sport)
    ).order_by(
        Tournament.created_at.desc()
    ).all()

    tournament_id = request.args.get(
        "tournament",
        type=int
    )

    tournament = None
    if tournament_id is not None:
        tournament = next(
            (t for t in tournaments if t.id == tournament_id),
            None
        )

    if tournament is None and tournaments:
        tournament = tournaments[0]

    if tournament is None:
        standings = []
        teams = []
        matches = []
        players = []
    else:
        teams = Team.query.options(
            joinedload(Team.sport)
        ).filter_by(
            tournament_id=tournament.id
        ).order_by(
            Team.name.asc()
        ).all()

        matches = Match.query.options(
            joinedload(Match.team1),
            joinedload(Match.team2)
        ).filter_by(
            tournament_id=tournament.id
        ).order_by(
            Match.date.asc()
        ).all()

        players = Player.query.join(Team).filter(
            Team.tournament_id == tournament.id
        ).order_by(
            Player.goals.desc()
        ).limit(5).all()

        standings = build_standings(teams, matches)

    return render_template(
        "index.html",

        tournaments=tournaments,
        tournament=tournament,
        standings=standings,
        teams=teams,
        matches=matches,
        players=players,
    )


def build_standings(teams, matches):

    standings = {}

    for team in teams:
        standings[team.id] = {
            "team": team,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "points": 0,
            "scored": 0,
            "conceded": 0,
            "goal_difference": 0
        }

    for match in matches:

        if match.status != "finished":
            continue

        if match.team1_id not in standings or match.team2_id not in standings:
            continue

        score1 = match.score1 or 0
        score2 = match.score2 or 0

        team1 = standings[match.team1_id]
        team2 = standings[match.team2_id]

        team1["scored"] += score1
        team1["conceded"] += score2
        team2["scored"] += score2
        team2["conceded"] += score1

        if score1 > score2:
            team1["wins"] += 1
            team2["losses"] += 1
            team1["points"] += 3
        elif score2 > score1:
            team2["wins"] += 1
            team1["losses"] += 1
            team2["points"] += 3
        else:
            team1["draws"] += 1
            team2["draws"] += 1
            team1["points"] += 1
            team2["points"] += 1

    for row in standings.values():
        row["goal_difference"] = row["scored"] - row["conceded"]

    standings_list = list(standings.values())

    standings_list.sort(
        key=lambda row: (
            -row["points"],
            -row["wins"],
            -row["goal_difference"],
            -row["scored"],
            row["team"].name
        )
    )

    return standings_list

@main.route("/api/tournament/<int:tournament_id>")
def tournament_data(tournament_id):

    tournament = Tournament.query.options(
        joinedload(Tournament.sport)
    ).filter_by(
        id=tournament_id
    ).first()

    if tournament is None:
        return jsonify({
            "error": "Tournament not found"
        }), 404

    teams = Team.query.options(
        joinedload(Team.sport)
    ).filter_by(
        tournament_id=tournament.id
    ).order_by(
        Team.name.asc()
    ).all()

    matches = Match.query.options(
        joinedload(Match.team1),
        joinedload(Match.team2)
    ).filter_by(
        tournament_id=tournament.id
    ).order_by(
        Match.date.asc()
    ).all()

    players = Player.query.join(Team).filter(
        Team.tournament_id == tournament.id
    ).order_by(
        Player.goals.desc()
    ).limit(5).all()

    standings = build_standings(teams, matches)

    return jsonify({

        "tournament": {
            "id": tournament.id,
            "name": tournament.name,
            "season": tournament.season,
            "status": tournament.status,
            "sport": tournament.sport.name if tournament.sport else None
        },

        "standings": [

            {
                "name": row["team"].name,
                "logo": row["team"].logo,
                "wins": row["wins"],
                "draws": row["draws"],
                "losses": row["losses"],
                "points": row["points"],
                "goal_difference": row["goal_difference"]
            }

            for row in standings
        ],

        "teams": [

            {
                "name": team.name,
                "sport": tournament.sport.name if tournament.sport else None,
                "logo": team.logo
            }

            for team in teams
        ],

        "matches": [

            {
                "team1": match.team1.name if match.team1 else "TBD",
                "team2": match.team2.name if match.team2 else "TBD",
                "score1": match.score1,
                "score2": match.score2,
                "date": match.date,
                "sport": tournament.sport.name if tournament.sport else None
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