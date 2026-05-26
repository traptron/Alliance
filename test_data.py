from app import create_app, db
from app.models import (
    Team,
    Player,
    Sport,
    Tournament,
    Match,
    SportStatDefinition,
    PlayerStat
)

app = create_app()

with app.app_context():

    # спорт: футбол
    football = Sport(
        name="Football",
        points_win=3,
        points_draw=1,
        points_loss=0,
        tie_breakers="points,wins,goal_difference,scored"
    )

    db.session.add(football)
    db.session.commit()

    # турнир: футбол
    football_tournament = Tournament(
        name="Alliance League",
        sport_id=football.id,
        season="2026",
        status="active"
    )

    db.session.add(football_tournament)
    db.session.commit()

    # команды
    team = Team(
        name="IT Football",
        sport_id=football.id,
        tournament_id=football_tournament.id
    )

    team2 = Team(
        name="Alliance United",
        sport_id=football.id,
        tournament_id=football_tournament.id
    )

    db.session.add(team)
    db.session.add(team2)
    db.session.commit()

    # игроки
    player = Player(
        name="Иван",
        team_id=team.id
    )

    player2 = Player(
        name="Павел",
        team_id=team2.id
    )

    db.session.add(player)
    db.session.add(player2)
    db.session.commit()

    # метрики: футбол
    stats = [
        SportStatDefinition(sport_id=football.id, metric_key="goals", label="Голы", unit="шт", scope="player", sort_priority=1),
        SportStatDefinition(sport_id=football.id, metric_key="assists", label="Передачи", unit="шт", scope="player", sort_priority=2)
    ]

    db.session.add_all(stats)
    db.session.commit()

    player_stats = [
        PlayerStat(player_id=player.id, tournament_id=football_tournament.id, metric_key="goals", value=5),
        PlayerStat(player_id=player.id, tournament_id=football_tournament.id, metric_key="assists", value=2),
        PlayerStat(player_id=player2.id, tournament_id=football_tournament.id, metric_key="goals", value=3)
    ]

    db.session.add_all(player_stats)
    db.session.commit()

    # матч
    match = Match(
        sport_id=football.id,
        tournament_id=football_tournament.id,
        team1_id=team.id,
        team2_id=team2.id,
        score1=2,
        score2=1,
        status="finished",
        date="2026-05-23"
    )

    db.session.add(match)
    db.session.commit()

    # спорт: баскетбол
    basketball = Sport(
        name="Basketball",
        points_win=2,
        points_draw=0,
        points_loss=0,
        tie_breakers="points,wins,goal_difference,scored"
    )

    db.session.add(basketball)
    db.session.commit()

    basketball_tournament = Tournament(
        name="Alliance Cup",
        sport_id=basketball.id,
        season="2026",
        status="active"
    )

    db.session.add(basketball_tournament)
    db.session.commit()

    hoops = Team(
        name="Alliance Hoops",
        sport_id=basketball.id,
        tournament_id=basketball_tournament.id
    )

    db.session.add(hoops)
    db.session.commit()

    baller = Player(
        name="Артем",
        team_id=hoops.id
    )

    db.session.add(baller)
    db.session.commit()

    basketball_stats = [
        SportStatDefinition(sport_id=basketball.id, metric_key="points", label="Очки", unit="pts", scope="player", sort_priority=1),
        SportStatDefinition(sport_id=basketball.id, metric_key="rebounds", label="Подборы", unit="reb", scope="player", sort_priority=2),
        SportStatDefinition(sport_id=basketball.id, metric_key="blocks", label="Блоки", unit="blk", scope="player", sort_priority=3),
        SportStatDefinition(sport_id=basketball.id, metric_key="fouls", label="Фолы", unit="pf", scope="player", sort_priority=4),
        SportStatDefinition(sport_id=basketball.id, metric_key="games", label="Игры", unit="g", scope="player", sort_priority=5)
    ]

    db.session.add_all(basketball_stats)
    db.session.commit()

    basketball_player_stats = [
        PlayerStat(player_id=baller.id, tournament_id=basketball_tournament.id, metric_key="points", value=84),
        PlayerStat(player_id=baller.id, tournament_id=basketball_tournament.id, metric_key="games", value=6),
        PlayerStat(player_id=baller.id, tournament_id=basketball_tournament.id, metric_key="rebounds", value=24),
        PlayerStat(player_id=baller.id, tournament_id=basketball_tournament.id, metric_key="blocks", value=6),
        PlayerStat(player_id=baller.id, tournament_id=basketball_tournament.id, metric_key="fouls", value=7)
    ]

    db.session.add_all(basketball_player_stats)
    db.session.commit()

    print("DONE")