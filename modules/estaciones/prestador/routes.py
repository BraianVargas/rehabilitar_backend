from flask import Flask, jsonify, request
import json
from datetime import datetime

from .controller import *
import apiOperacionesComunes,apiDB
from modules.estaciones.prestador import prestadorBP
from modules.usuarios.controller import nuevo_usuario

NOT_ALLOWED_EXTENSIONS = ['exe','zip','rar','sql','msi','py','cs']

@prestadorBP.before_request
def middle_verif_token():
    if request.headers['Content-Type'] != "application/json":
        if request.method == "POST":
            data = json.loads(request.values.get('json'))
            token = str(data['token'])
            if(len(token) != 100):
                return jsonify({'no':"No se envió token de usuario o no es correcto"}),404
            if not (apiOperacionesComunes.verificaToken(token)):
                return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})
        else:
            pass
    else:
        if request.method == "POST":
            token = request.json.get('token')
            if(len(token) != 100):
                return jsonify({'no':"No se envió token de usuario o no es correcto"}),404
            if not (apiOperacionesComunes.verificaToken(token)):
                return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})
        else:
            pass

@prestadorBP.route('/',methods=['GET'])
def index_prestadores():
    return "Prestadores"

@prestadorBP.route('/cargar_estudio', methods=['POST'])
def carga_estudio():
    if request.method == 'POST':
        data = json.loads(request.values.get('json'))
        uploaded_files = list((request.files).listvalues())[0]
        subidos=[]
        for file in uploaded_files:
            if file.filename != '':
                if file.filename.split('.')[1] in NOT_ALLOWED_EXTENSIONS:
                    return jsonify({"error":"Tipo de archivo no permitido"}),401
                
                # carga informe estudio
                id_informe = apiDB.consultaGuardar(f"insert into informe_estudio (id_turno, id_estudio, id_area, observaciones) values ({data['id_turno']},{data['id_estudio']},{data['id_area']},'{data['observaciones']}')")[0]['last_insert_id()']
                
                # genera archivo y carga en la tabla de arcivos y trae el token generado
                fecha=str(datetime.datetime.now().year) + "/"+ str(datetime.datetime.now().month)+ "/"+ str(datetime.datetime.now().day )
                destino="files/prestador/"+fecha +'/'+str(data['id_area'])+'/'+str(data['id_estudio'])+'/'
                token_file=store_file(file, destino, data)
                saved_file = apiDB.consultaGuardar(f"insert into fact_informe_area (id_informe, token_archivo) values ({int(id_informe)},'{token_file}') ")
                subidos.append(
                    {
                        "file_id":saved_file[0]['last_insert_id()'],
                        "filename":file.filename
                    } 
                )
            else:
                return jsonify({"error":"No se ha seleccionado ningun archivo"}),404
        return jsonify(subidos),200
        

@prestadorBP.route('/delete_upload',methods=['POST'])
def delete_file():
    data = json.loads(request.values.get('json'))
    try:
        apiDB.consultaUpdate(f"update archivos set deleted_at='{datetime.datetime.now()}' where id={data['id_archivo']};")
        return jsonify({"ok":"Archivo eliminado correctamente"}),200
    except:
        return jsonify({"error":"Ha ocurrido un error durante la eliminación del turno"}),500

@prestadorBP.route('/new', methods=['POST'])
def new_prestador():
    try:
        data = request.get_json()
        try:
            usuario_id = nuevo_usuario(data['usuario'])
            data['prestador']['usuario_id'] = usuario_id
            nuevo_prestador(data['prestador'])
        except Exception as e:
            return jsonify(e),500
    except:
        try:
            data = json.loads(request.values.get('json'))
        except Exception as e:
            return jsonify(e),500