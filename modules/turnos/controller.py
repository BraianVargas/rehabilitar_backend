import datetime, holidays, apiDB, string, secrets
import apiOperacionesComunes
from flask import jsonify

def verifica_habil_feriado(fecha):
    pais = "AR"  
    feriados = holidays.CountryHoliday(pais)
    fecha_dt = datetime.datetime.strptime(fecha, "%d/%m/%Y").date()
    print(fecha_dt)
    if fecha_dt in feriados:
        if fecha_dt.weekday() < 5:  # 0 es lunes, 4 es viernes
            return "habil"
    else:
        if fecha_dt.weekday() < 5:  # 0 es lunes, 4 es viernes
            return "habil"
        else:
            return "fin de semana"
    
def verifica_no_turno(paciente_id,empresa_id,fecha):
    turnos = apiDB.consultaSelect(f"select count(*) from turnos where paciente_id={paciente_id} and empresa_id='{empresa_id}' and fecha='{fecha}';")
    
    if int(turnos[0]['count(*)']) >= 1:
        return True
    else:
        return False


def verifica_disponibles(fecha):
    turnos = apiDB.consultaSelect(f"select count(*) from turnos where fecha = '{fecha}'")
    if int(turnos[0]['count(*)']) >= 30:
        return False
    else:
        return True

def getPaciente(paciente_id):
    paciente = apiDB.consultaSelect(f"select * from pacientes where id = '{paciente_id}'")
    return paciente

def cargaTurno(turno,filetoken, enlace_ddjj):
    apiDB.consultaGuardar(
        f"""insert into turnos (paciente_id,empresa_id,fecha,tipo_examen,created_at,file_token,observaciones,link_ddjj, tipo_ficha)
            values (
                {turno['paciente_id']},
                {turno['empresa_id']},
                '{turno['fecha']}',
                '{turno['tipo_examen']}',
                '{datetime.datetime.now()}',
                '{filetoken}',
                '{turno['observaciones']}',
                '{enlace_ddjj}',
                {int(turno['tipo_ficha'])}
            );
        """
        )
    return jsonify({'Ok':"El paciente fue guardado correctamente"}),200
    
def consulta_turno(today):
    query = apiDB.consultaSelect(f"SELECT * FROM turnos WHERE fecha = '{today}'")
    
    if query is not None:
        turnos = []
        for i in range(len(query)):
            turno = query[i]
            name = apiDB.consultaSelect(f"SELECT razonsocial FROM empresas WHERE id={turno['empresa_id']}")
            ficha = apiDB.consultaSelect(f"SELECT nombre_ficha FROM tipo_ficha WHERE id={turno['tipo_ficha_id']}")
            if len(name)!=0:
                empresa_name = name[0]['razonsocial']
            else:
                empresa_name = ''
            paciente = getPaciente(int(turno['paciente_id']))
            turno_info = {
                "turno_id": turno['id'],
                "empresa": empresa_name,
                "confirmado": turno['confirmado'],
                "asistio": turno['asistio'],
                "atendido": turno['atendido'],
                "paciente_id": paciente[0]['id'],
                "paciente_nombre": paciente[0]['nombres'],
                "paciente_apellido": paciente[0]['apellidos'],
                "documento": paciente[0]['documento'],
                "telefono": paciente[0]['telefono'],
                "fecha_turno": turno['fecha'],
                "tipo_turno": turno['tipo_examen'],
                "tipo_ficha": ficha[0]['nombre_ficha'] if len(ficha)>0 else '',
                "file_token":turno['file_token'],
                "enlace_ddjj":turno['link_ddjj'],
                "urgente":turno['urgente'],
                "orden_urgente":turno['orden_urgente'],
                "orden_turno":turno['orden_turno'],
                "observaciones":turno['observaciones']
            }
            turnos.append(turno_info)
        return turnos

def consulta_turno_existente(turno_id):
    turno = apiDB.consultaSelect(f"SELECT * FROM turnos where id = {turno_id}")
    if len(turno)!=0:
        return True
    else:
        return False
    
def delete_turno(turno_id):
    try:
        if consulta_turno_existente(turno_id) != False:
            apiDB.consultaUpdate(f"update turnos set deleted='1' where id ='{turno_id}';")
            return True
        else:
            return False
    except:
        return jsonify({"ERROR": "Ha ocurrido un error durante la ejecucion, reintente"}), 500
        
def get_ultimo_urgente(fecha_turno):
    try:
        urgente = apiDB.consultaSelect(f"SELECT MAX(orden_urgente) FROM turnos WHERE fecha='{fecha_turno}'")
        if len(urgente)>0:
            return urgente[0]['MAX(orden_urgente)']
        else:
            return 0
    except:
        return 0

def get_ultimo_turno(fecha_turno):
    try:
        no_urgente = apiDB.consultaSelect(f"SELECT MAX(orden_turno) FROM turnos WHERE fecha='{fecha_turno}'")
        if len(no_urgente)>0:
            return no_urgente[0]['MAX(orden_turno)']
        else:
            return 0
    except:
        return 0

def confirma_turno(turno_id, confirma):
    dataTurno = apiDB.consultaSelect(f"Select * from turnos where id = {turno_id}")
    if dataTurno != None:
        try:
            orden=int(get_ultimo_turno(dataTurno[0]['fecha']))+1
            apiDB.consultaUpdate(f"update turnos set orden_turno={orden}, confirmado={confirma} where id={turno_id};")
            return True
        except:
            return False
    else:
        return False
    
def set_asistido(turno_id, presente):
    dataTurno = apiDB.consultaSelect(f"Select * from turnos where id = {turno_id}")
    if dataTurno != None:
        try:
            apiDB.consultaUpdate(f"update turnos set asistio={presente} where id={turno_id};")
            return True
        except:
            return False
    else:
        return False
    
def set_atendido(turno_id, atendido):
    dataTurno = apiDB.consultaSelect(f"Select * from turnos where id = {turno_id}")
    if dataTurno != None:
        try:
            apiDB.consultaUpdate(f"update turnos set atendido={atendido} where id={turno_id};")
            return True
        except:
            return False
    else:
        return False
    
def set_urgente(turno_id,urgente):
    dataTurno = apiDB.consultaSelect(f"Select * from turnos where id = {turno_id}")
    if dataTurno != None:
        try:
            orden=int(get_ultimo_urgente(dataTurno[0]['fecha']))+1
            apiDB.consultaUpdate(f"update turnos set urgente={urgente}, orden_urgente={orden} where id={turno_id};")
            return True
        except:
            return False
    else:
        return False

def ordena_lista_turnos(turnos,tipo_orden="orden_turno"):
    ban = True
    while ban:
        ban=False
        for i in range(len(turnos)-1):
            if int(turnos[i][f'{tipo_orden}']) > int(turnos[i+1][f'{tipo_orden}']):
                turnos[i], turnos[i+1] = turnos[i+1], turnos[i]
                ban=True
    return turnos

def filtra_turnos(turnos):
    new_turnos = [turno for turno in turnos if turno['confirmado'] == 1]

    urgentes = [turno for turno in new_turnos if turno['urgente'] == 1]
    urgentes = ordena_lista_turnos(urgentes,"orden_urgente")
    no_urgentes = [turno for turno in new_turnos if turno['urgente'] == 0]
    no_urgentes = ordena_lista_turnos(no_urgentes)

    total_atendidos = sum(turno['atendido'] for turno in new_turnos)
    total_presentes = sum(turno['asistio'] for turno in new_turnos)

    return {
        "atendidos": total_atendidos,
        "presentes": total_presentes,
        "turnos": no_urgentes,
        "urgentes": urgentes
    }

def fileNameGen():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20))
    return password
