from flask import render_template, request
from sqlalchemy.orm import joinedload

from . import main
from ..models import Team, Match, Tournament, TournamentSport, TournamentRegistration
from .stats import build_standings, build_top_players


@main.route("/")
def home():
    tournaments = Tournament.query.options(
        joinedload(Tournament.tournament_sports).joinedload(TournamentSport.sport)
    ).order_by(
        Tournament.created_at.desc()
    ).all()

    return render_template(
        "home.html",
        tournaments=tournaments
    )


@main.route("/tournaments")
def tournaments():
    tournaments = Tournament.query.options(
        joinedload(Tournament.tournament_sports).joinedload(TournamentSport.sport)
    ).order_by(
        Tournament.created_at.desc()
    ).all()

    tournament_id = request.args.get(
        "tournament",
        type=int
    )

    tournament_sport_id = request.args.get(
        "sport",
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
        top_players = []
        tournament_sport = None
        tournament_sports = []
    else:
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
            standings = []
            teams = []
            matches = []
            top_players = []
        else:
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

    return render_template(
        "tournaments.html",
        tournaments=tournaments,
        tournament=tournament,
        tournament_sport=tournament_sport,
        tournament_sports=tournament_sports,
        standings=standings,
        teams=teams,
        matches=matches,
        players=top_players,
    )


@main.route("/teams")
def teams():
    return render_template("teams.html")


@main.route("/players")
def players():
    return render_template("players.html")


@main.route("/schedule")
def schedule():
    return render_template("schedule.html")


@main.route("/media")
def media():
    return render_template("media.html")


@main.route("/about")
def about():
    return render_template("about.html")
