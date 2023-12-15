from flask import request, jsonify, redirect, url_for
import json

from . import informesBP
from .controller import *
import apiOperacionesComunes


@informesBP.before_request
def middle_verif_token():
    if request.headers['Content-Type'] != "application/json":
        if request.method == "POST":
            data = json.loads(request.values.get('json'))
            token = str(data['token'])
            if(len(token) != 100):
                return jsonify({'no':"No se envió token de usuario o no es correcto"}),404
            if not (apiOperacionesComunes.verificaToken(token)):
                return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})
        else:
            pass
    else:
        if request.method == "POST":
            token = request.json.get('token')
            if(len(token) != 100):
                return jsonify({'no':"No se envió token de usuario o no es correcto"}),404
            if not (apiOperacionesComunes.verificaToken(token)):
                return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})
        else:
            pass


@informesBP.route('/campos/<int:_area_id>', methods=['POST'])
def get_campos(_area_id):
    campos = get_data_campos(_area_id)
    return jsonify(campos),200

@informesBP.route('/campos/<int:_area_id>/<int:_id_turno>/save', methods=['POST'])
def save_campos(_area_id, _id_turno):
    url_for('/estaciones/prestador/cargar_estudio')