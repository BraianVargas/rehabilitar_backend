from flask import request, abort, jsonify
import apiDB
from functools import wraps
import json

def nuevo_usuario(data):
    query = f"insert into users (username, password, name) values ('{data['username']}','{data['password']}','{data['name']}')"
    usuario_id = apiDB.consultaGuardar(query)[0]['last_insert_id()']
    return usuario_id

def verifica_roles(required_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                data = request.get_json()
            except:
                try:
                    data = json.loads(request.values.get('json'))
                except Exception as e:
                    return jsonify(e),500
            query = "SELECT * FROM users WHERE token = %s"
            usuario = apiDB.consultaSelect(query, (data['token'],))[0]
            
            roles_usuario = usuario['roles']

            if not any(role in roles_usuario for role in required_roles):
                return jsonify({"error":"Usuario no autorizado"}),403  # Forbidden

            return f(*args, **kwargs)

        return decorated_function

    return decorator
