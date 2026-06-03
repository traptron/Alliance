from app import create_app, db
from app.models import (
    Team,
    Player,
    Sport,
    Tournament,
    TournamentSport,
    TournamentRegistration,
    Match,
    SportStatDefinition,
    MatchPlayerStat
)

app = create_app()

with app.app_context():

    football = Sport(
        name="Football",
        points_win=3,
        points_draw=1,
        points_loss=0,
        tie_breakers="points,wins,goal_difference,scored"
    )

    basketball = Sport(
        name="Basketball",
        points_win=2,
        points_draw=0,
        points_loss=0,
        tie_breakers="points,wins,goal_difference,scored"
    )

    db.session.add_all([football, basketball])
    db.session.commit()

    rector_cup = Tournament(
        name="Кубок Ректора",
        season="2026",
        status="active"
    )

    db.session.add(rector_cup)
    db.session.commit()

    rector_football = TournamentSport(
        tournament_id=rector_cup.id,
        sport_id=football.id,
        status="active"
    )

    rector_basketball = TournamentSport(
        tournament_id=rector_cup.id,
        sport_id=basketball.id,
        status="active"
    )

    db.session.add_all([rector_football, rector_basketball])
    db.session.commit()

    team = Team(
        name="IT Football",
        sport_id=football.id
    )

    team2 = Team(
        name="Alliance United",
        sport_id=football.id
    )

    hoops = Team(
        name="Alliance Hoops",
        sport_id=basketball.id
    )

    db.session.add_all([team, team2, hoops])
    db.session.commit()

    registrations = [
        TournamentRegistration(tournament_sport_id=rector_football.id, team_id=team.id),
        TournamentRegistration(tournament_sport_id=rector_football.id, team_id=team2.id),
        TournamentRegistration(tournament_sport_id=rector_basketball.id, team_id=hoops.id)
    ]

    db.session.add_all(registrations)
    db.session.commit()

    player = Player(
        name="Иван",
        team_id=team.id
    )

    player2 = Player(
        name="Павел",
        team_id=team2.id
    )

    baller = Player(
        name="Артем",
        team_id=hoops.id
    )

    db.session.add_all([player, player2, baller])
    db.session.commit()

    football_stats = [
        SportStatDefinition(sport_id=football.id, metric_key="goals", label="Голы", unit="шт", scope="player", sort_priority=1),
        SportStatDefinition(sport_id=football.id, metric_key="assists", label="Передачи", unit="шт", scope="player", sort_priority=2)
    ]

    basketball_stats = [
        SportStatDefinition(sport_id=basketball.id, metric_key="points", label="Очки", unit="pts", scope="player", sort_priority=1),
        SportStatDefinition(sport_id=basketball.id, metric_key="rebounds", label="Подборы", unit="reb", scope="player", sort_priority=2),
        SportStatDefinition(sport_id=basketball.id, metric_key="blocks", label="Блоки", unit="blk", scope="player", sort_priority=3),
        SportStatDefinition(sport_id=basketball.id, metric_key="fouls", label="Фолы", unit="pf", scope="player", sort_priority=4),
        SportStatDefinition(sport_id=basketball.id, metric_key="games", label="Игры", unit="g", scope="player", sort_priority=5)
    ]

    db.session.add_all(football_stats + basketball_stats)
    db.session.commit()

    match = Match(
        tournament_sport_id=rector_football.id,
        team1_id=team.id,
        team2_id=team2.id,
        score1=2,
        score2=1,
        status="finished",
        date="2026-05-23"
    )

    db.session.add(match)
    db.session.commit()

    match2 = Match(
        tournament_sport_id=rector_basketball.id,
        team1_id=hoops.id,
        team2_id=None,
        score1=78,
        score2=70,
        status="finished",
        date="2026-05-24"
    )

    db.session.add(match2)
    db.session.commit()

    player_stats = [
        MatchPlayerStat(player_id=player.id, match_id=match.id, metric_key="goals", value=2),
        MatchPlayerStat(player_id=player.id, match_id=match.id, metric_key="assists", value=1),
        MatchPlayerStat(player_id=player2.id, match_id=match.id, metric_key="goals", value=1),
        MatchPlayerStat(player_id=baller.id, match_id=match2.id, metric_key="points", value=28),
        MatchPlayerStat(player_id=baller.id, match_id=match2.id, metric_key="games", value=1),
        MatchPlayerStat(player_id=baller.id, match_id=match2.id, metric_key="rebounds", value=8),
        MatchPlayerStat(player_id=baller.id, match_id=match2.id, metric_key="blocks", value=2),
        MatchPlayerStat(player_id=baller.id, match_id=match2.id, metric_key="fouls", value=3)
    ]

    db.session.add_all(player_stats)
    db.session.commit()

    print("DONE")