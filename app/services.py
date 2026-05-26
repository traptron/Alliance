from . import db


def update_match_result(match):

    team1 = match.team1
    team2 = match.team2

    sport = match.tournament.sport if match.tournament else None
    points_win = sport.points_win if sport else 3
    points_draw = sport.points_draw if sport else 1
    points_loss = sport.points_loss if sport else 0

    # победа team1
    if match.score1 > match.score2:

        team1.wins += 1
        team1.points += points_win

        team2.losses += 1
        team2.points += points_loss

    # победа team2
    elif match.score2 > match.score1:

        team2.wins += 1
        team2.points += points_win

        team1.losses += 1
        team1.points += points_loss

    # ничья
    else:

        team1.draws += 1
        team2.draws += 1

        team1.points += points_draw
        team2.points += points_draw

    db.session.commit()