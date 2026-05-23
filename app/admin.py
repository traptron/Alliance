import os

from flask import url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import ImageUploadField

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

            relative_path=""
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