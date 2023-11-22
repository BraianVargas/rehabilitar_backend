from flask import Flask, jsonify, request
import datetime,json

from .controller import *
import apiOperacionesComunes,apiDB
from modules.estaciones.prestador import prestadorBP

NOT_ALLOWED_EXTENSIONS = ['exe','zip','rar','sql','msi','py','cs']

@prestadorBP.before_request
def middle_verif_token():
    if request.method == "POST":
        token = request.json.get('token')
        if(len(token) != 100):
            return jsonify({'no':"No se envió token de usuario o no es correcto"}),404
        if not (apiOperacionesComunes.verificaToken(token)):
            return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})
    else:
        pass

@prestadorBP.route('/cargar_estudio', methods=['POST'])
def carga_estudio():
    sesion_token = request.json.get('json')['token']
    
    data = request.values.get('json')
    uploaded_file = request.files['file']
    archivo=uploaded_file.filename.split('.')[1]

    if archivo in NOT_ALLOWED_EXTENSIONS:
        return jsonify({"error":"Tipo de archivo no permitido"}),401
    # cuando sea get que traiga los archivos cargados con anterioridad

    fecha=str(datetime.now().year) + "/"+ str(datetime.now().month)+ "/"+ str(datetime.now().day )
    destino="files/prestador/" +str(data['tipo']).upper() +'/'+ fecha +'/'
    store_file(uploaded_file, destino, sesion_token)