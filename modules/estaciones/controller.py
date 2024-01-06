import apiDB
from modules.turnos.controller import get_turno_by_id


def get_areas_by_tipo_ficha(id_turno):
    areas_atendidas= []
    turno = get_turno_by_id(id_turno)
    areas = apiDB.consultaSelect("select * from area")
    query = f"select distinct area_id from fact_tipo_ficha where tipo_ficha_id = '{turno[0]['tipo_ficha_id']}'"
    fact_areas = apiDB.consultaSelect(query, (turno[0]['tipo_ficha_id']),)
    for area in areas:
        for ficha in fact_areas:
            if area['id'] == ficha['area_id']:
                areas_atendidas.append(area)
    return areas_atendidas

