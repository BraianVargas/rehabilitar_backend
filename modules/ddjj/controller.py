from flask import jsonify
import apiOperacionesComunes, apiDB
import string, secrets

def tokenGen():
    alphabet = string.ascii_letters + string.digits
    tk = ''.join(secrets.choice(alphabet) for i in range(20))
    return tk

def save_ddjj(data,paciente_id,empresa_id):
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
        query = f"insert into fact_ddjj (ddjj_id, paciente_id, empresa_id, token_ddjj) values ({ddjj_id[0]['last_insert_id()']},{paciente_id},{empresa_id},'{ddjj_token}')"
        apiDB.consultaGuardar(query)
        return jsonify({'Mensaje': 'Datos procesados exitosamente'}), 200

    except Exception as e:
        return jsonify({'Error': str(e)}), 500
    
def update_ddjj(ddjj_id=None,data=None):
    if ddjj_id!=None:
        keys = list(data.keys())
        values = list(data.values())
        # ---------- Arma la query ----------
        query = f'UPDATE ddjj SET '
        for index, (key, value) in enumerate(data.items()):
            if key != "id":
                if isinstance(value, bool) or isinstance(value, int) or isinstance(value, float):
                    query += f"{key}={value}" if index == len(data) - 1 else f"{key}={value}, "
                else:
                    query += f"{key}='{value}'" if index == len(data) - 1 else f"{key}='{value}', "
        query += f" WHERE id={ddjj_id};"

        apiDB.consultaUpdate(query)
        return jsonify({'Mensaje': 'Datos procesados exitosamente'}), 200
    
def get_ddjj_by_id(ddjj_id):
    query = "SELECT * FROM ddjj WHERE id = '%s'"
    result = apiDB.consultaSelect(query,(ddjj_id,))
    return result

def get_ddjj_paciente(paciente_id, empresa_id):
    query = f"SELECT ddjj_id FROM fact_ddjj WHERE paciente_id = {paciente_id} AND empresa_id = {empresa_id} ORDER BY id DESC LIMIT 1"
    id_ddjj = apiDB.consultaSelect(query)
    
    if len(id_ddjj) > 0:
        id_ddjj = int(id_ddjj[0]['ddjj_id'])
        ddjj_info = get_ddjj_by_id(int(id_ddjj))
        return ddjj_info
    else: 
        return None