from modules.turnos import turnosBP
from flask import Flask, jsonify, request
import datetime
from controller import *

import apiOperacionesComunes,apiDB


@turnosBP.route('/nuevo', methods=['GET'])
def nuevoTurno():
     token = request.json.get("token")

     try:
          if (len(token) != 100):
               return apiOperacionesComunes.respJson('no',"No se envió token de usuario o no es correcto",{})
          if(apiOperacionesComunes.verificaToken(token)): # Si existe usuario con token.
               paciente_id = request.json.get("turnos")['paciente_id']
               
               dd = request.json.get("turnos")['day']
               mm = request.json.get('turnos')["month"]
               yyyy = request.json.get("turnos")['year']
               
               fecha=f"{dd}/{mm}/{yyyy}"
               if 
               fecha_dt = datetime.date(yyyy,mm,dd)
               if (verifica_habil_feriado(fecha_dt) == "habil"):

               return  str(fecha)
               
     except:
          return "nuevo except"