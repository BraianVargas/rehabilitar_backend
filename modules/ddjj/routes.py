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


    except Exception as e:
        return jsonify({"Error": str(e)}, 500)

