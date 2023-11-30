from flask import jsonify
import apiDB
import datetime, secrets,string, os


ALLOWED_EXTENSIONS=['png','jpg','jpeg','jfif']
UPLOAD_FOLDER = 'informes/'
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#
# -------------- Generador de token de archivo --------------
#
def fileNameGen():
    alphabet = string.ascii_letters + string.digits
    tk = ''.join(secrets.choice(alphabet) for i in range(20))
    return tk

#
# -------------- Generador de token de archivo --------------
#
def store_file(file,destino,data):
    if not os.path.exists(destino):
        os.makedirs(destino)
    file_token = fileNameGen()
    extension=file.filename.split('.')[1]
    
    while (os.path.exists(destino + file_token + file.filename)):
        file_token = fileNameGen()
    file.save(os.path.join(destino, file_token +'.'+extension))
    id_usuario_creador =  apiDB.consultaSelect(f"select id from users where token='{data['token']}'")[0]

    try:
        apiDB.consultaGuardar(f"insert into archivos (original_filename,id_usuario_creador, token_archivo) values ('{file.filename}','{id_usuario_creador['id']}','{file_token}')")
        return file_token
    except Exception as e:
        return jsonify(e),500
    
#
# -------------- Devuelve los archivos cargados --------------
#
def get_uploaded_files(fecha,data):
    uploaded = []
    id_usuario_creador =  apiDB.consultaSelect(f"select id from users where token='{data['token']}'")[0]
    path = f"files/prestador/{str(fecha.year)}/{str(fecha.month)}/{str(fecha.day)}/{str(data['id_area'])}/{str(data['id_estudio'])}"
    archivos = os.listdir(path)
    query = f"select * from archivos where id_usuario_creador={int(id_usuario_creador['id'])} and DATE(created_at)='{fecha.year}-{fecha.month}-{fecha.day}';"
    response = apiDB.consultaSelect(query)
    #verificar archivo no eliminado en ddbb
    for archivo in archivos:
        for file in response:
            if (file['deleted_at'] == None) and (archivo.split('.')[0] == file['token_archivo']):
                data = {
                    "file_id":file['id'],
                    "filename":file['original_filename']
                } 
                uploaded.append(data)
    return uploaded

# 
# -------------- Carga Nuevo prestador --------------
# 
def nuevo_prestador(data):
    keys = []
    values = []
    query = f"insert into prestador ("
    for key, value in data.items():
        keys.append(key)
        values.append(value)

    for key in keys:
        if key == keys[-1]:
            query += f"{key}"
        else:
            query += f"{key},"
    query += ") VALUES ("

    for value in values:
        if value == values[-1]:
            if isinstance(value,int):
                query+=f"{value}"
            else:
                query += f"'{value}'"
        else:
            if isinstance(value,int):
                query+=f"{value},"
            else:
                query += f"'{value}',"
    query += ")"

    print(query)

    try:
        print(1)
        id_prestador = apiDB.consultaGuardar(query)[0]['last_insert_id()']
        print(id_prestador)
        if id_prestador != None:
            return jsonify({"ok":"Prestador creado correctamente"}),200
    except Exception as e:
        return jsonify(e),500


















# {
#     "token":"O81mHXzrr8GZqvd4XQFEqeZ7DgokveZmN8adz6CqnDKSLiS2EJsJxcxeq2CqCHmRvEYGMMRi7W9AsAxuJ2sN5AHG2pGigERDKFDm",
#     "usuario":{
#         "username":"prestador_01",
#         "password":"1234",
#         "name":"Prestador"
#     },
#     "prestador":{
#         "codigo":"01234",
#         "estado":true,
#         "tipo_doc":"dni",
#         "nro_doc":"41803952",
#         "apellido":"Juarez",
#         "nombre":"Pepito Miguel",
#         "token_firma":"h9ohsdafasdlfskñl",
#         "calle":"Manuyel Quiroga",
#         "localidad":"Villa Krawsi",
#         "provincia":"San Juana",
#         "codigo_postal":"5142",
#         "telefono_1":"26455123122",
#         "telefono_2":"",
#         "email":"",
#         "areas_id":[1,4,2,5],
#         "matricula":"vencida"
#     }
# }