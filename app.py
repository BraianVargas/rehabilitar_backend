import apiDB
import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS

from flask import send_file

from werkzeug.utils import secure_filename
from apiFileUpload import apiFileUpload
from apiInformes import apiInformes
from apiLogin import apiLogin
from apiEmpresas import apiEmpresas
from apiPacientes import apiPacientes
from modules.turnos import *
# from apiUsuarios import apiUsuarios
# from apiFeriados import apiFeriados
# from apiTiposTramites import apiTiposTramites



app = Flask(__name__)

app.register_blueprint(apiFileUpload, url_prefix='/fileUpload')
app.register_blueprint(apiInformes, url_prefix='/informes')
app.register_blueprint(apiLogin, url_prefix='/login')
app.register_blueprint(apiEmpresas, url_prefix='/empresas')
app.register_blueprint(apiPacientes, url_prefix='/pacientes')
app.register_blueprint(turnosBP, url_prefix='/turnos') 
# app.register_blueprint(apiTiposTramites, url_prefix='/tipostramites')
app.config['CORS_HEADERS'] = 'Content-Type'


CORS(app)

###################################################################################
#                               prueba retorno
###################################################################################
@app.route('/', methods=['get'])
def test():
    db = mysql.connector.connect(host=str(apiDB.server_host),
                             user=str(apiDB.server_user),
                             passwd=str(apiDB.server_passwd),
                             db=str(apiDB.server_db),
                             port=str(apiDB.server_port))


    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT VERSION();")

    result=cursor.fetchone()
    return jsonify(result)



if __name__ == '__main__':
   app.run(host='0.0.0.0',debug=True,port=5000)