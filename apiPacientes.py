import datetime
import errno
import json
import os
import secrets
import string
import apiOperacionesComunes,apiDB
from flask import Blueprint, request, jsonify

from werkzeug.utils import secure_filename
apiPacientes=Blueprint('apiPacientes',__name__)

    
@apiPacientes.route('/',methods=['POST'])            
def get_All():                
    #obtendo los datos que vienen en json
    token = request.json.get("token")
    #verifico token
    try:
        
        if len(token)!=100:
            return apiOperacionesComunes.respJson('no',"No se envió token de usuario o no es correcto",{})
        if not (apiOperacionesComunes.verificaToken(token)):
            return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})

    except:
        return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})
        
    listado= apiDB.consultaSelect("Select * from pacientes order by apellidos")
    return apiOperacionesComunes.respJson('yes',"Listado de pacientes",{'listado':listado})

@apiPacientes.route('/<int:_id>',methods=['POST'])            
def get_ById(_id):                
    #obtendo los datos que vienen en json
    token = request.json.get("token")
    #verifico token
    try:
        
        if len(token)!=100:
            return apiOperacionesComunes.respJson('no',"No se envió token de usuario o no es correcto",{})
        if not (apiOperacionesComunes.verificaToken(token)):
            return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})

    except:
        return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})
        
    listado= apiDB.consultaSelect("Select * from pacientes where id = %s",([_id]))
    return apiOperacionesComunes.respJson('yes',"Listado de paciente con id "+ str(_id),{'listado':listado})

@apiPacientes.route('/dni/<string:_doc>',methods=['POST'])            
def get_ByDoc(_doc):                
    #obtendo los datos que vienen en json
    token = request.json.get("token")
    #verifico token
    try:
        
        if len(token)!=100:
            return apiOperacionesComunes.respJson('no',"No se envió token de usuario o no es correcto",{})
        if not (apiOperacionesComunes.verificaToken(token)):
            return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})

    except:
        return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})
        
    listado= apiDB.consultaSelect("Select * from pacientes where documento = %s",([_doc]))
    return apiOperacionesComunes.respJson('yes',"Listado de empresas con cuit " + _doc,{'listado':listado})

@apiPacientes.route('/new',methods=['POST'])            
def new():
    #obtendo los datos que vienen en json
    token = request.json.get("token")
    data = request.json.get("data")
    apellidos = data["apellidos"]
    nombres = data["nombres"]
    documento = data["documento"] 
    celular = data["celular"] if data['celular'] != '' else None
    telefono = data["telefono"] if data['telefono'] != '' else None
    domicilio = data["domicilio"] if data['domicilio'] != '' else None
    fecha_nacimiento = data["fecha_nacimiento"] if data['fecha_nacimiento'] != '' else None
    #verifico token
    try:
        if len(token)!=100:
            return apiOperacionesComunes.respJson('no',"No se envió token de usuario o no es correcto",{})
        if not (apiOperacionesComunes.verificaToken(token)):
            return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})
    except:
        return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})
    
    data_paciente = apiDB.consultaSelect("Select * from pacientes where documento = %s",[(str(documento))])
    if len(data_paciente) == 0:
        apiDB.consultaGuardar("""insert into pacientes (
                apellidos,
                nombres,
                documento,
                celular,
                telefono,
                domicilio,
                fecha_nacimiento
            ) values (%s,%s,%s,%s,%s,%s,%s)""",([apellidos,nombres,documento,celular,telefono,domicilio,fecha_nacimiento]))
        return apiOperacionesComunes.respJson('yes',"El paciente fue guardado correctamente",{})
    else:
        return jsonify({'Prohibido':f"El usuario con documento {documento} ya fue cargado "}),401


@apiPacientes.route('/update/<int:_id_paciente>', methods=['POST'])
def edit_paciente(_id_paciente):
    # Obtengio los datos del paciente
    token = request.json.get('token')
    data = request.json.get('data')
    try:
        if (len(token) != 100):
            return jsonify({'no':"No se envió token de usuario o no es correcto"}),404
        if not (apiOperacionesComunes.verificaToken(token)):
            return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})
    except:
        return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})

    if data:
        apiDB.consultaUpdate(
            f"""update pacientes set 
                    apellidos = '{data['apellidos']}',
                    nombres = '{data['nombres']}',
                    documento = '{data['documento']}',
                    celular = '{data['celular']}',
                    telefono = '{data['telefono']}',
                    domicilio = '{data['domicilio']}',
                    fecha_nacimiento = '{data['fecha_nacimiento']}'
                where id='{_id_paciente}'"""
        )

        return apiOperacionesComunes.respJson('yes',"El paciente fue actualizado correctamente",{})
    else:
        return apiOperacionesComunes.respJson('no',"No se recibió info de paciente",{})