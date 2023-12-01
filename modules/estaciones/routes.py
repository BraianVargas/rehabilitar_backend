from flask import Flask, jsonify, request
from datetime import datetime

from .controller import *
import apiOperacionesComunes,apiDB
from modules.estaciones import estacionesBP


@estacionesBP.before_request
def middle_verif_token():
    if request.method == "POST":
        token = request.json.get('token')
        if(len(token) != 100):
            return jsonify({'no':"No se envió token de usuario o no es correcto"}),404
        if not (apiOperacionesComunes.verificaToken(token)):
            return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})
    else:
        pass

@estacionesBP.route('/finaliza_atencion', methods=['POST'])
def fin_atencion():
    data = request.get_json()
    try:
        apiDB.consultaGuardar(f"insert into fact_asistencia_estaciones (id_turno, id_area_atendida) values ({data['id_turno']},{data['id_area_atendida']}) ")
        return jsonify({"ok":"Atencion finalizada correctamente"}),200
    except:
        return jsonify({"error":"Ha ocurrido un error al finalizar la atencion, reintente"}),500

@estacionesBP.route('/get_areas_atendidas',methods=['POST'])
def get_areas_atendidas():
    data = request.get_json()
    try:
        dd = data['day']
        mm = data["month"]
        yyyy = data['year']
        fecha=f"{yyyy}-{mm}-{dd}"
        areas = apiDB.consultaSelect(f"select * from area")
        atendidas = apiDB.consultaSelect(f"select * from fact_asistencia_estaciones where id_turno = {data['id_turno']} and DATE(created_at)='{fecha}'")
        estado = False
        for area in areas:
            area['estado']=estado
            for atendida in atendidas:
                if int(atendida['id_area_atendida']) == int(area['id']):
                    estado = True
                    area['estado']=estado
            estado=False
        
        return jsonify(areas),200
    except:
        return jsonify({"error":"Ha ocurrido un error al consultar las areas, reintente"}),500