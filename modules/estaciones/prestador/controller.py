from flask import jsonify
import apiDB
import datetime, secrets,string, os


ALLOWED_EXTENSIONS=['png','jpg','jpeg','jfif']
UPLOAD_FOLDER = 'informes/'
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def fileNameGen():
    alphabet = string.ascii_letters + string.digits
    tk = ''.join(secrets.choice(alphabet) for i in range(20))
    return tk

def store_file(file,destino,session_token):
    if not os.path.exists(destino):
        os.makedirs(destino)
    
    file_token = fileNameGen()
    
    #si existe genero hasta que no
    while (os.path.exists(destino + fileToken + file)):
        fileToken = fileNameGen()
    id_usuario_creador =  apiDB.consultaSelect(f"select id from usuarios where token='{session_token}'")
    print(id_usuario_creador)
    try:
        apiDB.consultaGuardar(f"insert into archivos (id_usuario_creador, token_archivo)")
        pass
    except Exception as e:
        return jsonify(e),500