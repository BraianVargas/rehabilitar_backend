import apiDB
import mysql.connector
from flask import Blueprint,  jsonify, request
from flask_cors import CORS
import datetime

apiLogin=Blueprint('apiLogin',__name__)

CORS(apiLogin)

###################################################################################
#                               COMPRUEBA TOKEN
###################################################################################
@apiLogin.route('/token', methods=['POST'])
def token():
    #Compruebo token---------------------------------------------------------------------------
    print(request is None)
    try:
        if 'token' not in request.json:
            return jsonify({"success":"fail",'message': "not loged user"}), 200
    except:
            return jsonify({"success":"fail",'message': "not loged user"}), 200
    
    token=request.json.get('token', "")

    if token != "":
        resultado=apiDB.consultaSelect(f"Select * from users where token='{token}'")
        if (len(resultado))==0:
            return jsonify({"success":"fail",'message': "loged user"}), 200
        else:
            return jsonify({"success":"ok",'message': "loged user"}), 200
#------------------------------------------------------------------------------------------

###################################################################################
#                 LOGIN DE USUARIO (DEVUELVE TOKEN SI ES CORRECTO)
###################################################################################
@apiLogin.route('/', methods=['POST'])
def login():
    try:
        usrname=request.json.get("data")['username']
        password=request.json.get("data")['password']
    except:
        resultado=jsonify({"success":"fail",'message': "no envió usrname o pasword"})
        resultado.headers.add('Access-Control-Allow-Origin', '*')
        return resultado

    #cursor = db.cursor(dictionary=True)
    query='''SELECT 
    u.id,
    u.username,
    u.name,
    u.deleted,
    u.last_login FROM users u
    where username = %s and password= %s'''
    #cursor.execute(query,(usrname,password))
    try:
        result=apiDB.consultaSelect(query,(usrname,password)) #cursor.fetchall()
        if (len(result)) > 0:
            current_time = datetime.datetime.now()
            last_login=apiDB.consultaSelect(f"select last_login from users where id = '{result[0]['id']}'")
            current_token=apiDB.consultaSelect(f"select token from users where id = '{result[0]['id']}'")
            print(f"Current token: {current_token}")
            time_difference = current_time - last_login[0]['last_login']
            if(current_token[0]['token'])=='': #Es primer ingreso
                nuevotoken=apiDB.tokengen()

                print("Primer Ingreso")
                query="update users set token=%s,last_login=NOW() where id=%s"
                apiDB.consultaGuardar(query,(nuevotoken,str(result[0]['id'])))
                texto={"success":"yes","usuario":result[0],"token":nuevotoken}
                response=jsonify(texto)
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response,201
            else:
                print("Primer Ingreso else")

                if (int(time_difference.total_seconds()) > 3600): #pasó una hora desde el ultimo lógin 
                    nuevotoken=apiDB.tokengen()
                    query="update users set token=%s,last_login=NOW() where id=%s"
                    apiDB.consultaGuardar(query,(nuevotoken,str(result[0]['id'])))
                    texto={"success":"yes","usuario":result[0],"token":nuevotoken}
                    response=jsonify(texto)
                    response.headers.add('Access-Control-Allow-Origin', '*')
                    return response,201
                else:
                    print("Ingreso con token actual")
                    print(f"Current token 1: {current_token}")
                    print(int(time_difference.total_seconds()))
                    texto={"success":"yes","usuario":result[0],"token":current_token[0]['token']}
                    response=jsonify(texto)
                    response.headers.add('Access-Control-Allow-Origin', '*')
                    return response,201
                    
            #cursor.execute(query,(nuevotoken,result[0]['id']))
            #db.commit()
            apiDB.consultaGuardar(query,(nuevotoken,str(result[0]['id'])))
            response=jsonify(texto)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response,201
        else:
            return jsonify({'success': "no",'message':"Usuario o contraseña no valido"}), 401
    except mysql.connector.Error as err:
            return jsonify({'success': "no",'message':"Error " + format(err)}), 401
 
