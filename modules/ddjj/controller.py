from flask import jsonify
import apiOperacionesComunes, apiDB
import string, secrets

def tokenGen():
    alphabet = string.ascii_letters + string.digits
    tk = ''.join(secrets.choice(alphabet) for i in range(20))
    return tk

def save_ddjj(data,paciente_id):
    try:
        keys = list(data.keys())
        values = list(data.values())

        formatted_values = []
        for value in values:
            if isinstance(value, bool):
                formatted_values.append(str(value).lower())
            else:
                formatted_values.append(f'"{value}"')
        ddjj_token = tokenGen()
        query = f'INSERT INTO ddjj ({", ".join(keys)}, token) VALUES ({", ".join(formatted_values)}, "{ddjj_token}");'
        ddjj_id = apiDB.consultaGuardar(query)
        query = f"insert into fact_ddjj (ddjj_id, paciente_id, token_ddjj) values ({ddjj_id[0]['last_insert_id()']},{paciente_id},'{ddjj_token}')"
        apiDB.consultaGuardar(query)
        return jsonify({'Mensaje': 'Datos procesados exitosamente'}), 200

    except Exception as e:
        return jsonify({'Error': str(e)}), 500