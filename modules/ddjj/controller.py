from flask import jsonify
import apiOperacionesComunes, apiDB


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

        query = f'INSERT INTO ddjj ({", ".join(keys)}) VALUES ({", ".join(formatted_values)});'
        ddjj_id = apiDB.consultaGuardar(query)
        query = f"insert into fact_ddjj (ddjj_id, paciente_id) values ({paciente_id},{ddjj_id[0]['last_insert_id()']})"
        apiDB.consultaGuardar(query)
        return jsonify({'Mensaje': 'Datos procesados exitosamente'}), 200

    except Exception as e:
        return jsonify({'Error': str(e)}), 500