from app import create_app, db
from app.models import Team, Player, Sport, Tournament, Match

app = create_app()

with app.app_context():

    # спорт
    sport = Sport(
        name="Football"
    )

    db.session.add(sport)
    db.session.commit()

    # турнир
    tournament = Tournament(
        name="Alliance League",
        sport_id=sport.id,
        season="2026",
        status="active"
    )

    db.session.add(tournament)
    db.session.commit()

    # команды
    team = Team(
        name="IT Football",
        sport_id=sport.id,
        tournament_id=tournament.id
    )

    team2 = Team(
        name="Alliance United",
        sport_id=sport.id,
        tournament_id=tournament.id
    )

    db.session.add(team)
    db.session.add(team2)
    db.session.commit()

    # игрок
    player = Player(
        name="Иван",
        goals=5,
        assists=2,
        team_id=team.id
    )

    db.session.add(player)
    db.session.commit()

    # матч
    match = Match(
        sport_id=sport.id,
        tournament_id=tournament.id,
        team1_id=team.id,
        team2_id=team2.id,
        score1=2,
        score2=1,
        status="finished",
        date="2026-05-23"
    )

    db.session.add(match)
    db.session.commit()

    print("DONE")