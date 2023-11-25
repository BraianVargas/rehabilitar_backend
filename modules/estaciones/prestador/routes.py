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
            
            # carga informe estudio
            id_informe = apiDB.consultaGuardar(f"insert into informe_estudio (id_turno, id_estudio, id_area) values ({data['id_turno']},{data['id_estudio']},{data['id_area']},{data['observaciones']})")[0]['last_insert_id()']
            # genera archivo y carga en la tabla de arcivos y trae el token generado
            fecha=str(datetime.datetime.now().year) + "/"+ str(datetime.datetime.now().month)+ "/"+ str(datetime.datetime.now().day )
            destino="files/prestador/"+fecha +'/'+str(data['id_area'])+'/'+str(data['id_estudio'])+'/'
            token_file=store_file(uploaded_file, destino, data)
            apiDB.consultaGuardar(f"insert into fact_informe_area (id_informe, token_archivo) values ({int(id_informe)},'{token_file}') ")
            subidos = get_uploaded_files(datetime.date.today(),data)


            return jsonify(subidos),200
        else:
            return jsonify({"error":"No se ha seleccionado ningun archivo"}),404
        

@prestadorBP.route('/delete_upload',methods=['POST'])
def delete_file():
    data = json.loads(request.values.get('json'))
    try:
        print(f"update archivos set deleted_at='{str(datetime.datetime.now())}' where id={data['id_archivo']};")
        apiDB.consultaUpdate(f"update archivos set deleted_at='{datetime.datetime.now()}' where id={data['id_archivo']};")
        return jsonify({"ok":"Archivo eliminado correctamente"}),200
    except:
        return jsonify({"error":"Ha ocurrido un error durante la eliminación del turno"}),500

