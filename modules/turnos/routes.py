from modules.turnos import turnosBP
from flask import Flask, jsonify, request
import datetime
from .controller import *

import apiOperacionesComunes,apiDB
from .pdf import *


@turnosBP.route('/nuevo', methods=['GET'])
def nuevoTurno():
     token = request.json.get("token")

     try:
          if (len(token) != 100):
               return apiOperacionesComunes.respJson('no',"No se envió token de usuario o no es correcto",{})
          if(apiOperacionesComunes.verificaToken(token)): # Si existe usuario con token.
               paciente_id = request.json.get("turno")['paciente_id']
               tipo_examen = request.json.get("turno")['tipo_examen']
               dd = request.json.get("turno")['day']
               mm = request.json.get('turno')["month"]
               yyyy = request.json.get("turno")['year']

               fecha=f"{dd}/{mm}/{yyyy}"
               if (verifica_habil_feriado(fecha) == "habil"):
                    paciente = getPaciente(paciente_id)
                    nombre = f"{paciente[0]['nombres']} {paciente[0]['appellidos']}"
                    dni = paciente[0]['documento']
                    
                    genera_comprobante_turno(nombre, dni, fecha, tipo_examen)

                    return apiOperacionesComunes.respJson('yes',"Turno cargado correctamente",{})
               else:
                    return "None"
               
     except:
          return "nuevo except"