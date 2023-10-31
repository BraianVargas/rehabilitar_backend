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
    # Obtengio los datos del empresa
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
        # apiDB.consultaUpdate(
        #     f"""update empresas set 
        #             razonsocial = '{data["razonsocial"]}',
        #             cuit = '{data["cuit"]}',
        #             telefono = '{data["telefono"]}',
        #             direccion = '{data["domicilio"]}',
        #             mail = '{data["mail"]}',
        #             contacto = '{data["contacto"]}'
        #         where id='{_id_empresa}'"""
        # )
        print(f"""
                insert into empresas (razonsocial,cuit,telefono,domicilio,mail,contacto) 
                VALUES (
                    '{data['razonsocial']}',
                    '{data['cuit']}',
                    '{data['telefono']}',
                    '{data['domicilio']}',
                    '{data['mail']}',
                    '{data['contacto']}'
                )
                ON DUPLICATE KEY UPDATE
                razonsocial = VALUES(razonsocial),
                cuit = VALUES(cuit),
                telefono = VALUES(telefono),
                domicilio = VALUES(domicilio),
                mail = VALUES(mail),
                contacto = VALUES(contacto);
                """)

        return apiOperacionesComunes.respJson('yes',"La empresa fue actualizada correctamente",{})
    else:
        return apiOperacionesComunes.respJson('no',"No se recibió info de empresa",{})