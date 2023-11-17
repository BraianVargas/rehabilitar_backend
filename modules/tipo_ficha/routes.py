from flask import Flask, jsonify, request
import datetime,json


from .controller import *
import apiOperacionesComunes,apiDB
from modules.tipo_ficha import tipoFichaBP


@tipoFichaBP.before_request
def middle_verif_token():
    if request.method == "POST":
        token = request.json.get('token')
        if(len(token) != 100):
            return jsonify({'no':"No se envió token de usuario o no es correcto"}),404
        if not (apiOperacionesComunes.verificaToken(token)):
            return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})
    else:
        pass

@tipoFichaBP.route('/get_areas',methods=['POST'])
def get_areas():
    try:
        areas_json = get_areas_controller()
        return jsonify(areas_json),200
    except:
        return jsonify({"error":"no se ha podido consultar las areas, reintente"}),500

@tipoFichaBP.route('/get_estudios/by_area/<int:id_area>', methods=['POST'])
def get_estudios(id_area):
    try:
        if verifica_ficha_id(id_area):
            estudios_json = get_estudios_by_area_id_controller(id_area)
            return jsonify(estudios_json),200
    except: 
        return jsonify({"error":"no se ha podido consultar los estudios asociados al area seleccionada, reintente"}),500

@tipoFichaBP.route('/get_all',methods=['POST'])
def get_fichas():
    try:
        estudios_json = get_all_fichas_controller()
        return jsonify(estudios_json),200
    except: 
        return jsonify({"error":"no se ha podido consultar los estudios asociados al area seleccionada, reintente"}),500

@tipoFichaBP.route('/get_data_by_ficha/<int:ficha_id>', methods=['POST'])
def get_data_by_ficha(ficha_id):
    try:
        if verifica_ficha_id(ficha_id):
            areas_json = get_data_by_ficha_controller(ficha_id)
            return jsonify(areas_json),200
        else:
            return jsonify({"error":"Ficha inexistente en la ddbb"}), 500
    except:
        return jsonify({"error":"no se ha podido obtener la info para la ficha seleccionada, reintente"}),500


# @tipoFichaBP.route('/nueva', methods=['POST'])
# def crear_ficha():
#     # Nombre de ficha
#     # Area (1 o mas?)
#     # Examen/es 
#     data = request.get_json()

#     # data['areas'] puede ser una lista con los id de area
#     # data['estudios'] igual a data['areas']
