import datetime
import errno
import json
import os
import secrets
import string
import apiOperacionesComunes,apiDB
from flask import Blueprint, request

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
        
    apiDB.consultaGuardar("insert into empresas (razonsocial,cuit,domicilio,telefono,mail,contacto) values (%s,%s,%s,%s,%s,%s)",([razonsocial,cuit,direccion,telefono,mail,contacto]))
    return apiOperacionesComunes.respJson('yes',"La empresa fue guardada correctamente",{})