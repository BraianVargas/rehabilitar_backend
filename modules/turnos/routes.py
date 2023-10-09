from modules.turnos import turnosBP
from flask import Flask, jsonify, request
import datetime
from .controller import *
import json

import apiOperacionesComunes,apiDB
from .pdf import *


@turnosBP.route('/nuevo', methods=['GET','POST'])
def nuevoTurno():
     token = request.json.get("token")
     try:
          if (len(token) != 100):
               return apiOperacionesComunes.respJson('no',"No se envió token de usuario o no es correcto",{})
          if request.method == 'POST':
               if(apiOperacionesComunes.verificaToken(token)): # Si existe usuario con token.
                    paciente_id = request.json.get("turno")['paciente_id']
                    tipo_examen = request.json.get("turno")['tipo_examen']
                    dd = request.json.get("turno")['day']
                    mm = request.json.get('turno')["month"]
                    yyyy = request.json.get("turno")['year']
                    
                    fecha=f"{dd}/{mm}/{yyyy}"
                    fecha_dt = datetime.datetime.strptime(fecha, "%d/%m/%Y").date()
                    if verifica_no_turno(paciente_id, fecha_dt): # True si tiene turnos
                         return apiOperacionesComunes.respJson('no',f"El paciente ya posee turno para la fecha {fecha}",{})
                         
                    if (verifica_habil_feriado(fecha) == "habil"):
                         if (verifica_disponibles(fecha_dt) == True):
                              paciente = getPaciente(paciente_id)
                              nombre = f"{paciente[0]['nombres']} {paciente[0]['apellidos']}"
                              dni = paciente[0]['documento']
                              turno = {
                                   "paciente_id":paciente_id,
                                   "fecha":fecha_dt,
                                   "tipo_examen":tipo_examen, 
                              }
                              cargaTurno(turno)
                              genera_comprobante_turno(nombre, dni, fecha, tipo_examen)
                              return jsonify({"success": "Turno Cargado correctamente",}), 200
                              return apiOperacionesComunes.respJson('yes',"Turno cargado correctamente",{})
                         else:
                              print("token")
                              return apiOperacionesComunes.respJson('no',"No quedan turnos disponibles",{})
                    else:
                         return apiOperacionesComunes.respJson('no',"La fecha seleccionada no está habilitada para asignar turno",{})
               else:
                    return apiOperacionesComunes.respJson('no',"No se envió token de usuario o no es correcto",{})
     except:
          return apiOperacionesComunes.respJson('no',"Error inesperado",{})


@turnosBP.route('/today', methods=['GET','POST'])
def get_turnos_dia():
     token = request.json.get("token")
     try:
          if (len(token) != 100):
               return apiOperacionesComunes.respJson('no',"No se envió token de usuario o no es correcto",{})

          today_date = datetime.date.today()
          date = (str(today_date) + ' 00:00:00')
          print(date)
          fecha_dt = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date()
          print(fecha_dt)
          turnos = consulta_turno(fecha_dt)
          return turnos
     except:
          return jsonify({"Error": "Ha ocurrido un error durante la consulta",}), 500
     
