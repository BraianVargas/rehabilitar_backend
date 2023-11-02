from modules.turnos import turnosBP
from flask import Flask, jsonify, request, send_file
import datetime
from .controller import *

import apiOperacionesComunes,apiDB
from .pdf import *

@turnosBP.route('/nuevo', methods=['POST'])
def nuevoTurno():
     token = request.json.get("token")
     try:
          if (len(token) != 100):
               return jsonify({'no':"No se envió token de usuario o no es correcto"}),404
          if not (apiOperacionesComunes.verificaToken(token)):
               return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})
          if request.method == 'POST':
               paciente_id = request.json.get("turno")['paciente_id']
               empresa_id = request.json.get("turno")['empresa_id']
               tipo_examen = request.json.get("turno")['tipo_examen']
               observaciones = request.json.get("turno")['observaciones']
               dd = request.json.get("turno")['day']
               mm = request.json.get('turno')["month"]
               yyyy = request.json.get("turno")['year']
               fecha=f"{dd}/{mm}/{yyyy}"
               fecha_dt = datetime.datetime.strptime(fecha, "%d/%m/%Y").date()

               if verifica_no_turno(paciente_id, empresa_id, fecha_dt): # True si tiene turnos
                    return jsonify({'no':f"El paciente ya posee turno para la fecha {fecha}"}),405

               if (verifica_habil_feriado(fecha) == "habil"):
                    if (verifica_disponibles(fecha_dt) == True):
                         paciente = getPaciente(paciente_id)
                         nombre = f"{paciente[0]['nombres']} {paciente[0]['apellidos']}"
                         dni = paciente[0]['documento']
                         turno = {
                              "paciente_id":paciente_id,
                              "empresa_id":empresa_id,
                              "fecha":fecha_dt,
                              "tipo_examen":tipo_examen,
                              "observaciones":observaciones,
                         }
                         filetoken, enlace_ddjj = genera_comprobante_turno(nombre, dni, fecha, tipo_examen, empresa_id)
                         cargaTurno(turno, filetoken, enlace_ddjj)
                         return jsonify({"ok": "Turno cargado correctamente",}), 200
                    else:
                         return jsonify({'no':"No quedan turnos disponibles"}),405
               else:
                    return jsonify({'no':"La fecha seleccionada no está habilitada para asignar turno"}),401

     except:
          return jsonify({"no": "Ha ocurrido un error durante la consulta",}), 500



@turnosBP.route('/today', methods=['GET','POST'])
def get_turnos_dia():
     turnos = []
     token = request.json.get("token")
     try:
          if (len(token) != 100):
               return jsonify({'no':"No se envió token de usuario o no es correcto"}),404
          if not (apiOperacionesComunes.verificaToken(token)):
               return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})
          if request.method == "POST":
               today_date = datetime.date.today()
               date = (str(today_date) + ' 00:00:00')
               turnos = consulta_turno(date)
          return turnos
     except Exception as e:
          return jsonify({"no": f"{e}",}), 500


@turnosBP.route('/<string:_token>',methods=['GET'])
def get_informe(_token):
     dataTurno = apiDB.consultaSelect("Select * from turnos where binary file_token = %s",[(str(_token))])
     
     if len(dataTurno)>0:
          fecha = str(dataTurno[0]['fecha'].date())
          day = (fecha.split('-'))[2]
          month = (fecha.split('-'))[1]
          year = (fecha.split('-'))[0]
          paciente = getPaciente(int(dataTurno[0]['paciente_id']))
          current_directory = os.getcwd()
          file_directory = os.path.join(current_directory, 'turnos', dataTurno[0]['tipo_examen'].lower(), f"{day}-{month}-{year}")
          if not os.path.exists(file_directory):
               return jsonify({"error":"Archivo no encontrado o ruta de archivo inexistente."}),404
          turno = os.path.join(file_directory, f"{_token}.pdf")
          archivo =  send_file(turno, as_attachment=True,download_name=f"{paciente[0]['documento']}_{dataTurno[0]['tipo_examen']}_{fecha[0]}.pdf")
          return archivo
     else:
          return jsonify({"error":"Token de archivo no valido."}),404

@turnosBP.route('/delete', methods=['GET','POST'])
def del_turno():
     token = request.json.get('token')
     try:
          if(len(token) != 100):
               return jsonify({'no':"No se envió token de usuario o no es correcto"}),404
          if not (apiOperacionesComunes.verificaToken(token)):
               return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})
          status = (bool(delete_turno(request.json.get('turno_id'))))
          if status == True:
               return jsonify({'ok':"Turno eliminado correctamente"}),200
          else:
               return jsonify({'no': "El turno seleccionado no se encontro o no existe"}),500
     except:
          return jsonify({"no": "Ha ocurrido un error durante la ejecucion, reintente"}), 500


@turnosBP.route('/confirma', methods=["POST"])
def conf_turno():
     token = request.json.get('token')
     try:
          if(len(token) != 100):
               return jsonify({'no':"No se envió token de usuario o no es correcto"}),404
          if not (apiOperacionesComunes.verificaToken(token)):
               return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})
          turno_id = request.json.get('turno_id')
          confirma = request.json.get('confirma')

          status = confirma_turno(turno_id,confirma)
          if status == True:
               return jsonify({'ok':"Turno confirmado correctamente"}),200
          else:
               return jsonify({'no': "El turno seleccionado no se actualizo correctamente"}),500
     except:
          return jsonify({"no": "Ha ocurrido un error durante la ejecucion, reintente"}), 500