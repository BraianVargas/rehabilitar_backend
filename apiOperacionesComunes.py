from flask import jsonify
import apiDB
import datetime


def respJson(exito,mensaje,datos):
    return jsonify({'success': exito,'message':mensaje,'data':datos})

def verificaToken(token):
    if token != "":
        resultado=apiDB.consultaSelect(f"Select * from users where binary token='{token}'")
        if (len(resultado))==0:
            return False
        else:
            return True
#------------------------------------------------------------------------------------------
# def verifica_actividad():
#         current_time = datetime.datetime.now()
#         result=apiDB.consultaSelect(query,(usrname,password)) #cursor.fetchall()
#         last_login=apiDB.consultaSelect(f"select last_login from users where id = '{result[0]['id']}'")
#         current_token=apiDB.consultaSelect(f"select token from users where id = '{result[0]['id']}'")
#         time_difference = current_time - last_login[0]['last_login']

#         if (int(time_difference.total_seconds()) > 3600): #pasó una hora desde el ultimo lógin 
#             nuevotoken=apiDB.tokengen()
#             query="update users set token=%s,last_login=NOW() where id=%s"
#             apiDB.consultaGuardar(query,(nuevotoken,str(result[0]['id'])))
#             texto={"success":"yes","usuario":result[0],"token":nuevotoken}
#             response=jsonify(texto)
#             response.headers.add('Access-Control-Allow-Origin', '*')
#             return response,201