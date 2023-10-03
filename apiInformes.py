import datetime
import errno
import json
import os
import secrets
import string
import apiOperacionesComunes,apiDB
from flask import Blueprint, request, send_file

from werkzeug.utils import secure_filename
apiInformes=Blueprint('apiInformes',__name__)

    
@apiInformes.route('/<string:_token>',methods=['GET'])            
def get_informe(_token):                
    dbData = apiDB.consultaSelect("Select * from informes where binary token = %s",[(str(_token))])
    informe="informes/" + str(dbData[0]["fechahora"].year) + "/" + str(dbData[0]["fechahora"].month)  + "/" +  str(dbData[0]["fechahora"].day)  + "/" + _token  +  ".pdf"
    
    return send_file(informe, as_attachment=True,download_name="informe.pdf")
