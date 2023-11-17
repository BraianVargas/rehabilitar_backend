import apiDB

# **********************************************************
#            VERIFICA FICHA ID
# **********************************************************
def verifica_ficha_id(ficha_id):
    data = apiDB.consultaSelect(f"Select * from tipo_ficha where id={int(ficha_id)}")
    if len(data) > 0:
        return True
    else:
        return False
    
# **********************************************************
#            VERIFICA AREA ID
# **********************************************************
def verifica_area_id(area_id):
    data = apiDB.consultaSelect(f"Select * from area where id={int(area_id)}")
    if len(data) > 0:
        return True
    else:
        return False


def get_all_fichas_controller():
    query = "SELECT * FROM tipo_ficha"
    return apiDB.consultaSelect(query)

def get_areas_controller():
    query = "SELECT * FROM area"
    return apiDB.consultaSelect(query)

def get_areas_by_id_controller(area_id):
    query = "SELECT * FROM area WHERE id = %s"
    return apiDB.consultaSelect(query, (int(area_id),))

def get_estudios_by_area_id_controller(id_area):
    query = "SELECT * FROM estudios WHERE id_area = %s"
    return apiDB.consultaSelect(query, (int(id_area),))

def get_data_by_ficha_controller(ficha_id):
    query = f"SELECT area_id FROM fact_tipo_ficha WHERE tipo_ficha_id={ficha_id};"
    result = apiDB.consultaSelect(query)

    area_ids = [dato['area_id'] for dato in result]
    data = {}

    for area_id in area_ids:
        area = get_areas_by_id_controller(area_id)
        if area:
            area_info = area[0]
            estudios = get_estudios_by_area_id_controller(int(area_info['id']))
            info = {area_info['Descripcion']: estudios}
            data.update(info)

    return data


    return data
