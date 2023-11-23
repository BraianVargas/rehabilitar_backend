from flask import Flask, jsonify, request
import json
from datetime import datetime

from .controller import *
import apiOperacionesComunes,apiDB
from modules.estaciones.prestador import prestadorBP

NOT_ALLOWED_EXTENSIONS = ['exe','zip','rar','sql','msi','py','cs']

@prestadorBP.before_request
def middle_verif_token():
    if request.method == "POST":
        data = json.loads(request.values.get('json'))
        token = str(data['token'])
        if(len(token) != 100):
            return jsonify({'no':"No se envió token de usuario o no es correcto"}),404
        if not (apiOperacionesComunes.verificaToken(token)):
            return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})
    else:
        pass

@prestadorBP.route('/cargar_estudio', methods=['POST'])
def carga_estudio():
    if request.method == 'POST':
        data = json.loads(request.values.get('json'))
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            if uploaded_file.filename.split('.')[1] in NOT_ALLOWED_EXTENSIONS:
                return jsonify({"error":"Tipo de archivo no permitido"}),401
            fecha=str(datetime.datetime.now().year) + "/"+ str(datetime.datetime.now().month)+ "/"+ str(datetime.datetime.now().day )
            destino="files/prestador/"+fecha +'/'+str(data['id_area'])+'/'+str(data['id_estudio'])+'/'
            store_file(uploaded_file, destino, data)
            return jsonify(get_uploaded_files(datetime.date.today(),data)),200
        else:
            return jsonify({"error":"No se ha seleccionado ningun archivo"}),404
