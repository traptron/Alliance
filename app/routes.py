from flask import Blueprint, render_template, request, redirect, url_for, jsonify

from flask_login import (
    login_user,
    logout_user,
    login_required
)

from werkzeug.security import check_password_hash

from sqlalchemy import func
from sqlalchemy.orm import joinedload

from .models import Team, Match, Player, User, Tournament, SportStatDefinition, PlayerStat

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
        top_players = []
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

        standings = build_standings(teams, matches, tournament.sport)
        top_players = build_top_players(tournament)

    return render_template(
        "index.html",

        tournaments=tournaments,
        tournament=tournament,
        standings=standings,
        teams=teams,
        matches=matches,
        players=top_players,
    )


def build_standings(teams, matches, sport):

    points_win = sport.points_win if sport else 3
    points_draw = sport.points_draw if sport else 1
    points_loss = sport.points_loss if sport else 0
    tie_breakers = parse_tie_breakers(sport)

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
            team1["points"] += points_win
            team2["points"] += points_loss
        elif score2 > score1:
            team2["wins"] += 1
            team1["losses"] += 1
            team2["points"] += points_win
            team1["points"] += points_loss
        else:
            team1["draws"] += 1
            team2["draws"] += 1
            team1["points"] += points_draw
            team2["points"] += points_draw

    for row in standings.values():
        row["goal_difference"] = row["scored"] - row["conceded"]

    standings_list = list(standings.values())

    standings_list.sort(
        key=lambda row: build_standings_sort_key(row, tie_breakers)
    )

    return standings_list


def parse_tie_breakers(sport):

    default_order = [
        "points",
        "wins",
        "goal_difference",
        "scored"
    ]

    if not sport or not sport.tie_breakers:
        return default_order

    order = [
        item.strip() for item in sport.tie_breakers.split(",")
        if item.strip()
    ]

    return order or default_order


def build_standings_sort_key(row, tie_breakers):

    key = []

    for breaker in tie_breakers:
        if breaker == "team_name":
            key.append(row["team"].name)
        else:
            key.append(-row.get(breaker, 0))

    key.append(row["team"].name)
    return tuple(key)


def get_player_stat_totals(tournament_id, metric_key):

    rows = (
        PlayerStat.query
        .with_entities(
            Player.id.label("player_id"),
            Player.name.label("player_name"),
            Team.name.label("team_name"),
            func.sum(PlayerStat.value).label("total")
        )
        .join(Player, PlayerStat.player_id == Player.id)
        .join(Team, Player.team_id == Team.id)
        .filter(
            PlayerStat.tournament_id == tournament_id,
            PlayerStat.metric_key == metric_key
        )
        .group_by(Player.id, Player.name, Team.name)
        .all()
    )

    return {
        row.player_id: {
            "name": row.player_name,
            "team": row.team_name,
            "value": float(row.total or 0)
        }
        for row in rows
    }


def build_top_players(tournament):

    sport = tournament.sport
    if not sport:
        return []

    metric_defs = SportStatDefinition.query.filter_by(
        sport_id=sport.id,
        scope="player"
    ).order_by(
        SportStatDefinition.sort_priority.asc()
    ).all()

    label_map = {stat.metric_key: stat.label for stat in metric_defs}

    sport_name = sport.name.lower()

    if "basket" in sport_name:
        points = get_player_stat_totals(tournament.id, "points")
        games = get_player_stat_totals(tournament.id, "games")

        players = []

        for player_id, data in points.items():
            game_count = games.get(player_id, {}).get("value", 0)
            ppg = data["value"] / game_count if game_count else 0

            players.append({
                "name": data["name"],
                "team": data["team"],
                "primary_value": round(ppg, 2),
                "primary_label": "PPG"
            })

        players.sort(
            key=lambda row: row["primary_value"],
            reverse=True
        )

        return players[:5]

    goals = get_player_stat_totals(tournament.id, "goals")

    players = [
        {
            "name": data["name"],
            "team": data["team"],
            "primary_value": int(data["value"]),
            "primary_label": label_map.get("goals", "Голы")
        }
        for data in goals.values()
    ]

    players.sort(
        key=lambda row: row["primary_value"],
        reverse=True
    )

    return players[:5]

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

    standings = build_standings(teams, matches, tournament.sport)
    top_players = build_top_players(tournament)

    stat_definitions = SportStatDefinition.query.filter_by(
        sport_id=tournament.sport.id,
        scope="player"
    ).order_by(
        SportStatDefinition.sort_priority.asc()
    ).all() if tournament.sport else []

    return jsonify({

        "tournament": {
            "id": tournament.id,
            "name": tournament.name,
            "season": tournament.season,
            "status": tournament.status,
            "sport": tournament.sport.name if tournament.sport else None,
            "rules": {
                "points_win": tournament.sport.points_win if tournament.sport else 3,
                "points_draw": tournament.sport.points_draw if tournament.sport else 1,
                "points_loss": tournament.sport.points_loss if tournament.sport else 0,
                "tie_breakers": parse_tie_breakers(tournament.sport)
            }
        },

        "stat_definitions": [
            {
                "metric_key": stat.metric_key,
                "label": stat.label,
                "unit": stat.unit,
                "scope": stat.scope
            }
            for stat in stat_definitions
        ],

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

        "players": top_players
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