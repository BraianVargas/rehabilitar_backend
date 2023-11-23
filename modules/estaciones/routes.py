from flask import Flask, jsonify, request
from datetime import datetime

from .controller import *
import apiOperacionesComunes,apiDB
from modules.estaciones import estacionesBP



@estacionesBP.route('/finaliza_atencion', methods=['POST'])
def fin_atencion():
    values = request.get_json()
    return None