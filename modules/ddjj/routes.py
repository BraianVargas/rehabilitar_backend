from flask import Flask, request, jsonify

import apiOperacionesComunes, apiDB

from modules.ddjj import ddjjBP
from .controller import *

@ddjjBP.route('/<int:_dni>', methods=['GET', 'POST'])
def ddjj_paciente(_dni):
    try:
        token = request.json.get('token')
        if len(token) != 100:
            return jsonify({'Error': "No se envió token de usuario o no es correcto"}), 404

        if request.method == 'POST':
            datos_frontend = request.json.get("data", {})
            resultado = procesar_datos(_dni, token, datos_frontend)

            return resultado

    except Exception as e:
        return jsonify({"Error": str(e)}, 500)

    data_paciente = apiDB.consultaSelect("Select * from pacientes where documento = %s", [(str(_dni))])

    return data_paciente