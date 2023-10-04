from flask import Blueprint

turnosBP = Blueprint('turnos_BP', __name__)

from . import routes