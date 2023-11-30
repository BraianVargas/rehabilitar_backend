from flask import Blueprint

usuariosBP = Blueprint('usuarios_BP',__name__)

from . import routes