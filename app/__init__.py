from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_admin import Admin

from flask_login import LoginManager

db = SQLAlchemy()

admin_site = Admin(
    name="ССК Альянс Admin"
)

login_manager = LoginManager()

def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = "secret"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

    db.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = "main.login"

    # импорт моделей
    from .models import Team, Player, Match, Sport, Tournament

    # Flask-Admin

    from .admin import AdminModelView, TeamAdminView, MatchAdminView, TournamentAdminView

    admin_site.init_app(app)

    admin_site.add_view(TeamAdminView(Team, db.session))

    admin_site.add_view(AdminModelView(Player, db.session))

    admin_site.add_view(TournamentAdminView(Tournament, db.session))

    admin_site.add_view(MatchAdminView(Match, db.session))

    admin_site.add_view(AdminModelView(Sport, db.session))
    

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # routes
    from .routes import main

    app.register_blueprint(main)

    return app

