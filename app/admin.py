import os
import uuid

from flask import url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import ImageUploadField

from werkzeug.utils import secure_filename

from flask_login import current_user

from .services import update_match_result

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

        if model.status == "finished":

            update_match_result(model)


class TournamentAdminView(AdminModelView):
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


class PlayerStatAdminView(AdminModelView):
    column_list = [
        "player",
        "tournament",
        "metric_key",
        "value"
    ]