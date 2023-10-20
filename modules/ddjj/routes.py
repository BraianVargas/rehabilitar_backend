from flask import Flask, request, jsonify

import apiOperacionesComunes, apiDB

from modules.ddjj import ddjjBP
from .controller import *


@ddjjBP.route('/<int:_dni>', methods=['GET', 'POST'])
def ddjj_paciente(_dni):
    try:
        if request.method == 'POST':
            paciente_id = apiDB.consultaSelect("Select id from pacientes where documento = %s", [(str(_dni))])
            print(paciente_id)
            token = request.json.get('token')
            data = request.json.get('data')
            if paciente_id != []:
                status = save_ddjj(data,paciente_id[0]['id'])
                return status
            else:
                return jsonify({'Error': "Paciente no encontrado"}), 500
        else:
            paciente = apiDB.consultaSelect("Select * from pacientes where documento = %s", [(str(_dni))])
            return jsonify(paciente)

    except Exception as e:
        return jsonify({"Error": str(e)}, 500)

@ddjjBP.route('/consulta', methods=["GET","POST"])
def consulta_ddjj():
    try:
        if request.method == 'POST':
            token = request.json.get('token')   
            _dni = request.json.get('dni')
            if(len(token) != 100):
                return jsonify({'Error':"No se envió token de usuario o no es correcto"}),404
            paciente = apiDB.consultaSelect("Select * from pacientes where documento = %s", [(str(_dni))])
            ddjj_id = apiDB.consultaSelect("Select id from fact_ddjj where paciente_id = %s", [(str(paciente[0]['id']))])
            ddjj = apiDB.consultaSelect("Select * from ddjj where id = %s", [(str(ddjj_id[-1]['id']))])
            return jsonify(ddjj)
        else:
            pass
    except Exception as e:
        return jsonify({"Error": str(e)}, 500)