import datetime
import holidays
import apiDB
import apiOperacionesComunes
from flask import jsonify

def verifica_habil_feriado(fecha):
    pais = "AR"  
    feriados = holidays.CountryHoliday(pais)
    fecha_dt = datetime.datetime.strptime(fecha, "%d/%m/%Y").date()
    
    if fecha_dt in feriados:
        return "feriado"
    else:
        if fecha_dt.weekday() < 5:  # 0 es lunes, 4 es viernes
            return "habil"
        else:
            return "fin de semana"
    
def verifica_no_turno(paciente_id,fecha):
    turnos = apiDB.consultaSelect(f"select count(*) from turnos where paciente_id = {paciente_id} and fecha = '{fecha}'")
    
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

def cargaTurno(turno):
    apiDB.consultaGuardar(
        f"""insert into turnos (paciente_id,fecha,tipo_examen) values (
            {turno['paciente_id']},'{turno['fecha']}','{turno['tipo_examen']}'
            );
        """
        )
    return jsonify({'Ok',"El paciente fue guardado correctamente"}),200
    
def consulta_turno(today):
    query = apiDB.consultaSelect(f"SELECT * FROM turnos WHERE fecha = '{today}'")
    if query is not None:
        turnos = []
        for i in range(len(query)):
            turno = query[i]
            paciente = getPaciente(int(turno['paciente_id']))
            turno_info = {
                "paciente_nombre": paciente[0]['nombres'],
                "paciente_apellido": paciente[0]['apellidos'],
                "documento": paciente[0]['documento'],
                "fecha_turno": turno['fecha'],
                "tipo_turno": turno['tipo_examen']
            }
            turnos.append(turno_info)
        return turnos
