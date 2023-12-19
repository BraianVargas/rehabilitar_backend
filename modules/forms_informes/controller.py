from flask import jsonify

import apiDB

def get_data_campos(id_area, categoria):
    query = "select * from campos where id_area = '%s' and categoria_form = %s"
    campos = apiDB.consultaSelect(query, (id_area, categoria))
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

def save_info_campos(data, _id_turno):
    final_data = []
    for info in data:
        query = "INSERT INTO campos_informacion (id_campo, id_turno, value, id_adjunto) values (%s,%s,%s,%s)"
        apiDB.consultaGuardar(query, (info['campo_id'], _id_turno, info['value'],str(list(info['id_adjunto']))))
        data_to_save = {
            "campo_id" : info['campo_id'],
            "id_turno" : _id_turno,
            "value" : info['value'],
            "id_adjunto" : info['id_adjunto']
        }
        final_data.append(data_to_save)

    return final_data