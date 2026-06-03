import os
import uuid

from flask import url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import ImageUploadField

from werkzeug.utils import secure_filename

from flask_login import current_user

from .models import TournamentRegistration

class AdminModelView(ModelView):

    def is_accessible(self):

        return current_user.is_authenticated


class TeamAdminView(AdminModelView):

    form_extra_fields = {

        "logo": ImageUploadField(
            "Logo",

            base_path="app/static/uploads",

            relative_path="",

            namegen=lambda obj, file_data: (
                f"{uuid.uuid4().hex}"
                f"{os.path.splitext(secure_filename(file_data.filename))[1].lower()}"
            )
        )
    }

class MatchAdminView(AdminModelView):

    def on_model_change(
        self,
        form,
        model,
        is_created
    ):

        tournament_sport = model.tournament_sport
        if tournament_sport and tournament_sport.sport_id:
            if model.team1 and model.team1.sport_id != tournament_sport.sport_id:
                raise ValueError("Team 1 sport does not match tournament sport")
            if model.team2 and model.team2.sport_id != tournament_sport.sport_id:
                raise ValueError("Team 2 sport does not match tournament sport")

            if model.team1:
                exists = TournamentRegistration.query.filter_by(
                    tournament_sport_id=tournament_sport.id,
                    team_id=model.team1.id
                ).first()
                if not exists:
                    raise ValueError("Team 1 is not registered in this tournament")

            if model.team2:
                exists = TournamentRegistration.query.filter_by(
                    tournament_sport_id=tournament_sport.id,
                    team_id=model.team2.id
                ).first()
                if not exists:
                    raise ValueError("Team 2 is not registered in this tournament")

        return None


class TournamentAdminView(AdminModelView):
    pass


class TournamentSportAdminView(AdminModelView):
    pass


class TournamentRegistrationAdminView(AdminModelView):
    pass


class SportStatDefinitionAdminView(AdminModelView):
    column_list = [
        "sport",
        "metric_key",
        "label",
        "unit",
        "scope",
        "sort_priority"
    ]


class MatchPlayerStatAdminView(AdminModelView):
    column_list = [
        "match",
        "player",
        "metric_key",
        "value"
    ]