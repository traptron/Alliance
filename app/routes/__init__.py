from flask import Blueprint

main = Blueprint("main", __name__)

from . import views  # noqa: F401
from . import api  # noqa: F401
from . import auth  # noqa: F401

__all__ = ["main"]
