import datetime
import errno
import json
import os
import secrets
import string
import apiOperacionesComunes,apiDB
from flask import Blueprint, request, jsonify

from werkzeug.utils import secure_filename
apiEmpresas=Blueprint('apiEmpresas',__name__)

    
@apiEmpresas.route('/',methods=['POST'])            
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
        
    listado= apiDB.consultaSelect("Select * from empresas order by razonsocial")
    return apiOperacionesComunes.respJson('yes',"Listado de empresas",{'listado':listado})

@apiEmpresas.route('/<int:_id>',methods=['POST'])            
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
        
    listado= apiDB.consultaSelect("Select * from empresas where id = %s",([_id]))
    return apiOperacionesComunes.respJson('yes',"Listado de empresas con id "+ str(_id),{'listado':listado})

@apiEmpresas.route('/cuit/<string:_cuit>',methods=['POST'])            
def get_ByCuit(_cuit):                
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
        
    listado= apiDB.consultaSelect("Select * from empresas where cuit = %s",([_cuit]))
    return apiOperacionesComunes.respJson('yes',"Listado de empresas con cuit " + _cuit,{'listado':listado})

@apiEmpresas.route('/new',methods=['POST'])            
def new():                
    #obtendo los datos que vienen en json
    token = request.json.get("token")
    data = request.json.get("data")
    razonsocial=data["razonsocial"]
    cuit=data["cuit"]
    telefono=data["telefono"]
    direccion=data["domicilio"]
    mail   =data["mail"]
    contacto=data["contacto"]
    #verifico token
    try:
        if len(token)!=100:
            return apiOperacionesComunes.respJson('no',"No se envió token de usuario o no es correcto",{})
        if not (apiOperacionesComunes.verificaToken(token)):
            return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})
    except:
        return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})
    
    # VERIFICO RAZONSOCIAL NO CREADA
    try:
        empresa = apiDB.consultaSelect(f"select * from empresas where razonsocial='{razonsocial}'")
        if len(empresa)!=0:
            return jsonify({"error":"La empresa se cargo con anterioridad."}),401
        else:
            apiDB.consultaGuardar("insert into empresas (razonsocial,cuit,domicilio,telefono,mail,contacto) values (%s,%s,%s,%s,%s,%s)",([razonsocial,cuit,direccion,telefono,mail,contacto]))
            return apiOperacionesComunes.respJson('yes',"La empresa fue guardada correctamente",{})
    except:
        return jsonify({"error":"ocurrio un error durante la consulta."}), 500
    
@apiEmpresas.route('/update/<int:_id_empresa>', methods=['POST'])
def edit_empresa(_id_empresa):
    # Obtain the user token and data from the request
    token = request.json.get('token')
    data = request.json.get('data')
    
    try:
        # Check token validity and length
        if not token or len(token) != 100 or not apiOperacionesComunes.verificaToken(token):
            return jsonify({'error': 'El token no es correcto o ha expirado'}), 404
    except Exception as e:
        return jsonify({'error': 'El token no es correcto o ha expirado'}), 404

    if data:
        new_razonsocial = data.get('razonsocial')
        if new_razonsocial:
            existing_razonsocial = apiDB.consultaSelect(f"SELECT razonsocial FROM empresas WHERE razonsocial = %s", (new_razonsocial,))
            if existing_razonsocial:
                return jsonify({'error': 'La razón social ingresada ya existe.'}), 401
            query = """UPDATE empresas
                    SET razonsocial = %s,
                        cuit = %s,
                        telefono = %s,
                        domicilio = %s,
                        mail = %s,
                        contacto = %s
                    WHERE id = %s"""
            params = (data['razonsocial'], data['cuit'], data['telefono'], data['domicilio'], data['mail'], data['contacto'], _id_empresa)
            apiDB.consultaUpdate(query, params)

            return jsonify({'message': 'La empresa fue actualizada correctamente'}), 200
        else:
            return jsonify({'error': 'No se recibió información de la empresa'}), 400
    else:
        return jsonify({'error': 'No se recibió información de la empresa'}), 400
