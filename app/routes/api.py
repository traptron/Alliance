from flask import jsonify, request
from sqlalchemy.orm import joinedload

from . import main

from ..models import Team, Match, Tournament, TournamentSport, TournamentRegistration, SportStatDefinition
from .stats import build_standings, build_top_players, parse_tie_breakers


@main.route("/api/tournament/<int:tournament_id>")
def tournament_data(tournament_id):
    tournament = Tournament.query.options(
        joinedload(Tournament.tournament_sports).joinedload(TournamentSport.sport)
    ).filter_by(
        id=tournament_id
    ).first()

    if tournament is None:
        return jsonify({
            "error": "Tournament not found"
        }), 404

    tournament_sport_id = request.args.get(
        "sport",
        type=int
    )

    tournament_sports = sorted(
        list(tournament.tournament_sports or []),
        key=lambda ts: ts.sport.name if ts.sport else ""
    )
    tournament_sport = None

    if tournament_sport_id is not None:
        tournament_sport = next(
            (ts for ts in tournament_sports if ts.id == tournament_sport_id),
            None
        )

    if tournament_sport is None and tournament_sports:
        tournament_sport = tournament_sports[0]

    if tournament_sport is None:
        return jsonify({
            "error": "Tournament sport not found"
        }), 404

    teams = (
        Team.query
        .join(TournamentRegistration, TournamentRegistration.team_id == Team.id)
        .filter(TournamentRegistration.tournament_sport_id == tournament_sport.id)
        .order_by(Team.name.asc())
        .all()
    )

    matches = Match.query.options(
        joinedload(Match.team1),
        joinedload(Match.team2)
    ).filter_by(
        tournament_sport_id=tournament_sport.id
    ).order_by(
        Match.date.asc()
    ).all()

    standings = build_standings(teams, matches, tournament_sport.sport)
    top_players = build_top_players(tournament_sport)

    stat_definitions = SportStatDefinition.query.filter_by(
        sport_id=tournament_sport.sport.id,
        scope="player"
    ).order_by(
        SportStatDefinition.sort_priority.asc()
    ).all() if tournament_sport.sport else []

    return jsonify({

        "tournament": {
            "id": tournament.id,
            "name": tournament.name,
            "season": tournament.season,
            "status": tournament.status,
            "sport": tournament_sport.sport.name if tournament_sport.sport else None,
            "tournament_sport_id": tournament_sport.id,
            "rules": {
                "points_win": tournament_sport.sport.points_win if tournament_sport.sport else 3,
                "points_draw": tournament_sport.sport.points_draw if tournament_sport.sport else 1,
                "points_loss": tournament_sport.sport.points_loss if tournament_sport.sport else 0,
                "tie_breakers": parse_tie_breakers(tournament_sport.sport)
            }
        },

        "sports": [
            {
                "id": ts.id,
                "sport_id": ts.sport.id if ts.sport else None,
                "name": ts.sport.name if ts.sport else "—",
                "status": ts.status
            }
            for ts in tournament_sports
        ],

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
                "sport": tournament_sport.sport.name if tournament_sport.sport else None,
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
                "sport": tournament_sport.sport.name if tournament_sport.sport else None,
                "status": match.status
            }

            for match in matches
        ],

        "players": top_players
    })
