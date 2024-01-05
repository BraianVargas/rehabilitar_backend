import apiDB
from modules.turnos.controller import get_turno_by_id


def get_areas_by_tipo_ficha(id_turno):
    turno = get_turno_by_id(id_turno)
    query = f"select distinct area_id from fact_tipo_ficha where tipo_ficha_id = '{turno[0]['tipo_ficha_id']}'"
    areas = apiDB.consultaSelect(query, (turno[0]['tipo_ficha_id']),)
    
    return areas
