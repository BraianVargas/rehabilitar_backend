from flask import jsonify
import json

from ..turnos.controller import *
from ..ddjj.controller import *
from .pdf import *
import apiDB

def get_data_campos(id_area, categoria):
    if id_area == 2:
        query = "select * from campos where id_area = '%s' and categoria = %s"
        campos = apiDB.consultaSelect(query, (id_area, categoria,))
    else:
        query = "select * from campos where id_area = '%s'"
        campos = apiDB.consultaSelect(query, (id_area,))

    result = []
    for campo in campos:
        options = json.loads(campo["options"]) if campo['options'] is not None else None

        campos_dict={
            "campo_id":campo["id"],
            "id_area":campo["id_area"],
            "name":campo["name"],
            "label":campo["label"],
            "type":campo["type"],
            "clase":campo["clase"],
            "options": options,
            "default_value":campo["default_value"],
            "form_orden":campo["form_orden"],
            "id_turno":None,
            "value":None,
            "id_adjunto":None
        }
        result.append(campos_dict)
    return result

def save_info_campos(data, _id_turno, _id_area, categoria):
    final_data = []
    for info in data:
        if (_id_area == 2):
            query = "INSERT INTO campos_informacion (id_campo, id_turno, value, id_adjunto,observaciones) values (%s,%s,%s,%s,%s)"
            apiDB.consultaGuardar(query,(
                info['campo_id'],
                _id_turno,
                info['value'],
                str(list(info['id_adjunto'])) if info['id_adjunto']!=None else '' ,
                str(categoria)
                )
            )
        else:
            query = "INSERT INTO campos_informacion (id_campo, id_turno, value, id_adjunto) values (%s,%s,%s,%s)"
            apiDB.consultaGuardar(query, (info['campo_id'], _id_turno, info['value'],str(list(info['id_adjunto']))))
        data_to_save = {
            "campo_id" : info['campo_id'],
            "id_turno" : _id_turno,
            "value" : info['value'],
            "id_adjunto" : str(list(info['id_adjunto'])) if info['id_adjunto']!=None else '',
            "categoria":categoria
        }
        final_data.append(data_to_save)

    return final_data

def get_info_paciente(id_paciente):
    query = "SELECT * FROM pacientes WHERE id = '%s'"
    result = apiDB.consultaSelect(query,(id_paciente,))
    return result
    
def get_info_empresa(id_empresa):
    query = "SELECT * FROM empresas WHERE id = '%s'"
    result = apiDB.consultaSelect(query,(id_empresa,))
    return result

def get_info_campos_by_turno(id_turno):
    query = f"SELECT * FROM campos_informacion INNER JOIN campos ON id_campo = campos.id WHERE id_turno = '%s'"
    info_campo = apiDB.consultaSelect(query,(int(id_turno),))
    return info_campo

def generate_pdf(info_turno,info_paciente,info_empresa,ddjj_paciente,info_campos):
    if info_turno['deleted']!= None:
        return jsonify({"error":"El turno seleccionado fué eliminado"}),401
    if ddjj_paciente != None:
        genera_ddjj(info_turno,info_paciente,ddjj_paciente)
    genera_consentimiento(info_paciente, info_turno)
    genera_clinico(info_campos, info_paciente, info_turno)
    return True

def dataCatch_pdfGenerator(id_turno):
    info_turno = get_turno_by_id(id_turno)[0]
    info_paciente = get_info_paciente(info_turno['paciente_id'])[0]
    info_empresa = get_info_empresa(info_turno['empresa_id'])[0]
    ddjj_paciente = get_ddjj_paciente(info_turno['paciente_id'], info_turno['empresa_id'])
    info_campos = get_info_campos_by_turno(info_turno['id'])

    status = generate_pdf(info_turno,info_paciente,info_empresa,ddjj_paciente,info_campos)
    return status



