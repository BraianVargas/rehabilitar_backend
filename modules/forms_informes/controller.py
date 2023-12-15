from flask import jsonify

import apiDB

def get_data_campos(id_area):
    query = "select * from campos where id_area = '%s'"
    campos = apiDB.consultaSelect(query, (id_area,))
    result = []
    for campo in campos:
        campos_dict={
            "campo_id":campo["id"],
            "id_area":campo["id_area"],
            "name":campo["name"],
            "label":campo["label"],
            "type":campo["type"],
            "options":campo["options"],
            "default_value":campo["default_value"],
            "form_orden":campo["form_orden"],
            "id_turno":None,
            "value":None,
            "id_adjunto":None
        }
        result.append(campos_dict)
    return result
