from . import db


def update_match_result(match):

    team1 = match.team1
    team2 = match.team2

    # победа team1
    if match.score1 > match.score2:

        team1.wins += 1
        team1.points += 3

        team2.losses += 1

    # победа team2
    elif match.score2 > match.score1:

        team2.wins += 1
        team2.points += 3

        team1.losses += 1

    # ничья
    else:

        team1.draws += 1
        team2.draws += 1

        team1.points += 1
        team2.points += 1

    db.session.commit()