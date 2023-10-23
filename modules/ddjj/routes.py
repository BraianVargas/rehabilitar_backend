from flask import Flask, request, jsonify

import apiOperacionesComunes, apiDB

from modules.ddjj import ddjjBP
from .controller import *


@ddjjBP.route('/nueva', methods=['GET', 'POST'])
def ddjj_paciente():
    try:
        if request.method == 'POST':
            _dni = request.args.get('dni')
            _empresa_id = request.args.get('empresa_id')
            paciente_id = apiDB.consultaSelect("Select id from pacientes where documento = %s", [(str(_dni))])
            
            data = request.json.get('data')
            
            if paciente_id != []:
                status = save_ddjj(data,paciente_id[0]['id'],_empresa_id)
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
            _empresa_id = request.json.get('empresa_id')

            if(len(token) != 100):
                return jsonify({'Error':"No se envió token de usuario o no es correcto"}),404
            if not (apiOperacionesComunes.verificaToken(token)):
                return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})
            

            paciente = apiDB.consultaSelect("Select * from pacientes where documento = %s", [(str(_dni))])
            ddjj_token = apiDB.consultaSelect("Select token_ddjj from fact_ddjj where paciente_id=%s and empresa_id=%s", [(str(paciente[0]['id'])),(str(_empresa_id))])
            ddjj = apiDB.consultaSelect("Select * from ddjj where token = %s", [(str(ddjj_token[0]['token_ddjj']))])
            return jsonify({
                "paciente":paciente[0],
                "data_ddjj":ddjj[0]
            })
        else:
            pass
    except Exception as e:
        return jsonify({"Error": str(e)}, 500)