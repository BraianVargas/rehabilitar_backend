import datetime, secrets,string


ALLOWED_EXTENSIONS=['png','jpg','jpeg','jfif']
UPLOAD_FOLDER = 'informes/'
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


###################################################################################
#              GENERA UN TOKEN UNICO PARA EL USUARIO QUE HACE LOGIN
###################################################################################
def fileNameGen():
    alphabet = string.ascii_letters + string.digits
    tk = ''.join(secrets.choice(alphabet) for i in range(20))
    return tk
