import datetime
import errno
import json
import os
import secrets
import string
import apiOperacionesComunes,apiDB
from flask import Blueprint, request

from werkzeug.utils import secure_filename
apiFileUpload=Blueprint('apiFileUpload',__name__)

ALLOWED_EXTENSIONS = ['pdf']
  
UPLOAD_FOLDER = 'informes/'
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


###################################################################################
#              GENERA UN TOKEN UNICO PARA EL USUARIO QUE HACE LOGIN
###################################################################################
def fileNameGen():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20))
    return password

    
@apiFileUpload.route('/',methods=['POST'])            
def test_api():                
    fecha=str(datetime.datetime.now().year) + "/"+ str(datetime.datetime.now().month)+ "/"+ str(datetime.datetime.now().day )
    informePath='informes/'+ fecha  + "/"            
    #obtengo el informe             
    uploaded_file = request.files['document']
    archivo=uploaded_file.filename.split('.')[1]
    
    #verifico que sea pdf
    if archivo not in ALLOWED_EXTENSIONS:
        return apiOperacionesComunes.respJson('no',"Solo la extension pdf es permitida",{})
    
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
    
    #genero el directorio    
    try:
        #os.mkdir('informes')
        os.makedirs(informePath, exist_ok=True)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    
    #verifico existencia de archivo
    fileToken = fileNameGen()
    
    #si existe genero hasta que no
    while (os.path.exists(informePath + fileToken + '.pdf')):
        fileToken = fileNameGen()
    
    #guardo el archivo en la carpeta informes
    uploaded_file.save(os.path.join(informePath, fileToken + '.pdf'))
    
    #guardo en la base de datos los archivos con su respectivo token
    apiDB.consultaGuardar("insert into informes (token,empresa_id,paciente_id,fechahora) values (%s,%s,%s,%s)",(fileToken,data["data"]["empresa"],data["data"]["paciente"],datetime.datetime.now()))

    return apiOperacionesComunes.respJson('yes',"Los datos se guerdaron correctamente",{'fileToken':fileToken,"fecha":fecha})

