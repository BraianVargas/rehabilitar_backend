from flask import jsonify
import apiDB
import datetime


def respJson(exito,mensaje,datos):
    return jsonify({'success': exito,'message':mensaje,'data':datos})


def verifica_actividad(user, token):
    last_activity = apiDB.consultaSelect(f"SELECT last_activity FROM users WHERE token = '{user[0]['token']}'")[0]['last_activity']
    current_time = datetime.datetime.now()
    time_difference = (current_time - last_activity).total_seconds()

    if time_difference > 3600:  # Pasó una hora desde la última actividad
        return False
    else:
        apiDB.consultaUpdate(f"UPDATE users SET last_activity = NOW() WHERE token = '{token}'")
        return True

def verificaToken(token):
    if token:
        usuario = apiDB.consultaSelect(f"SELECT * FROM users WHERE binary token = '{token}'")

        if usuario:
            return verifica_actividad(usuario, token)

    return False