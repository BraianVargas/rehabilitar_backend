from flask import Blueprint

estacionesBP = Blueprint('estaciones_BP',__name__)

from . import routes