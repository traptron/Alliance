from app import create_app, db
from app.models import Institute, Team, Player

app = create_app()

with app.app_context():

    # институт
    institute = Institute(
        name="ИТ",
        points=10
    )

    db.session.add(institute)
    db.session.commit()

    # команда
    team = Team(
        name="IT Football",
        sport="Football",
        institute_id=institute.id
    )

    db.session.add(team)
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

    print("DONE")