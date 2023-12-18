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
    if request.headers['Content-Type'] == 'application/json':
        data = request.get_json()
    else:
        data = json.loads(request.values.get('json'))
    data = data['campos']
    print(data)
    input()
    final_data = []
    for info in data:
        query = "INSERT INTO campos_informacion (id_campo, id_turno, value, id_adjunto) values (%s,%s,%s,%s)"
        apiDB.consultaGuardar(query, (info['campo_id'], _id_turno, info['value'],str(list(info['id_adjunto']))))
        data_to_save = {
            "campo_id" : info['campo_id'],
            "id_turno" : _id_turno,
            "value" : info['value'],
            "id_adjunto" : info['id_adjunto']
        }
        final_data.append(data_to_save)
    return final_data

@informesBP.route('/campos/<int:_id_turno>/get_info', methods=['POST'])
def get_info(_id_turno):
    query = f"SELECT * FROM campos_informacion INNER JOIN campos ON id_campo = campos.id WHERE id_turno = {_id_turno}"
    result = apiDB.consultaSelect(query)
    return jsonify(result),200

@informesBP.route('/campos/<int:_id_turno>/get_informe', methods = ['POST'])
def get_informe(_id_turno):
    pass