from flask import Blueprint

prestadorBP = Blueprint('prestador_BP',__name__)

from . import routes