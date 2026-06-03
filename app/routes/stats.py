from sqlalchemy import func

from ..models import Player, Team, SportStatDefinition, MatchPlayerStat, Match


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


def get_player_stat_totals(tournament_sport_id, metric_key):

    rows = (
        MatchPlayerStat.query
        .with_entities(
            Player.id.label("player_id"),
            Player.name.label("player_name"),
            Team.name.label("team_name"),
            func.sum(MatchPlayerStat.value).label("total")
        )
        .join(Player, MatchPlayerStat.player_id == Player.id)
        .join(Team, Player.team_id == Team.id)
        .join(Match, MatchPlayerStat.match_id == Match.id)
        .filter(
            Match.tournament_sport_id == tournament_sport_id,
            MatchPlayerStat.metric_key == metric_key
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


def build_top_players(tournament_sport):

    sport = tournament_sport.sport if tournament_sport else None
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
        points = get_player_stat_totals(tournament_sport.id, "points")
        games = get_player_stat_totals(tournament_sport.id, "games")

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

    goals = get_player_stat_totals(tournament_sport.id, "goals")

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
