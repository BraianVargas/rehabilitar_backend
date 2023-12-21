from modules.imagenes import upload_fotosBP
from flask import Flask, jsonify, request, send_file
import datetime,json
from .controller import *
from datetime import datetime
import os
import apiOperacionesComunes,apiDB

ALLOWED_TYPES = ["firma","foto"]

@upload_fotosBP.route('/',methods=['POST'])            
def upload_photo():
    #obtendo los datos que vienen en json
    data = json.loads(request.values.get('json'))
    #verifico token
    try:
        token=data['token']
        if len(token)!=100:
            return apiOperacionesComunes.respJson('no',"No se envió token de usuario o no es correcto",{})
        if not (apiOperacionesComunes.verificaToken(token)):
            return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})
    except:
        return apiOperacionesComunes.respJson('no',"El token no es correcto o a expirado",{})
    #obtengo el informe
    uploaded_photo = request.files['image']
    archivo=uploaded_photo.filename.split('.')[1]
    
    #verifico que sea imagen
    if archivo not in ALLOWED_EXTENSIONS:
        return apiOperacionesComunes.respJson('no',"Solo la extension 'png','jpg','jpeg' y 'jfif' son permitidas",{})
    
    pacientes = apiDB.consultaSelect(f"select * from pacientes where id = {data['paciente_id']}")
    if data['tipo'] in ALLOWED_TYPES:
        fecha=apiDB.consultaSelect("SELECT fecha FROM turnos WHERE id='%s'",(int(data['turno_id']),))[0]['fecha'].date()
        fecha=str(fecha.year) + "/"+ str(fecha.month)+ "/"+ str(fecha.day )
        destino=  "files/imagenes/" +str(data['tipo']).upper() +'/'+ fecha +'/'+ pacientes[0]['documento']
    else:
        return jsonify({"error":f"Tipo de carga no válido. Tipos permitidos: {ALLOWED_TYPES}"})
    if not os.path.exists(destino):
        os.makedirs(destino)

    #verifico existencia de archivo
    fileToken = fileNameGen()
    
    #si existe genero hasta que no
    while (os.path.exists(destino + fileToken + archivo)):
        fileToken = fileNameGen()
    
    #guardo en la base de datos los archivos con su respectivo token
    try:
        if data['tipo'] == "foto":
            apiDB.consultaUpdate(f"update turnos set img_token='{fileToken}' where id={data['turno_id']} and paciente_id={data['paciente_id']}")
        if data['tipo'] == "firma":
            apiDB.consultaUpdate(f"update turnos set firma_token='{fileToken}' where id={data['turno_id']} and paciente_id={data['paciente_id']}")
        #guardo el archivo en la carpeta informes
        uploaded_photo.save(os.path.join(destino, fileToken +'.'+archivo))
        return apiOperacionesComunes.respJson('yes',"Los datos se guerdaron correctamente",{'fileToken':fileToken,"fecha":fecha})
    except Exception as e:
        return jsonify(e),500