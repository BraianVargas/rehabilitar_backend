import datetime
import holidays
import apiDB

def verifica_habil_feriado(fecha):
    pais = "AR"  
    feriados = holidays.CountryHoliday(pais)
    fecha_dt = datetime.datetime.strptime(fecha, "%d/%m/%Y").date()
    print(fecha_dt)
    if fecha_dt in feriados:
        return "feriado"
    else:
        if fecha_dt.weekday() < 5:  # 0 es lunes, 4 es viernes
            return "habil"
        else:
            return "fin de semana"
    


def getPaciente(paciente_id):
    paciente = apiDB.consultaSelect(f"Select * from pacientes where id = '{paciente_id}'")
    return paciente

def cargaTurno(turno):
    
    apiDB.consultaGuardar("""insert into turnos (
            apellidos,
            nombres,
            documento,
            celular,
            telefono,
            domicilio,
            fecha_nacimiento
        ) values (%s,%s,%s,%s,%s,%s,%s)""",([apellidos,nombres,documento,celular,telefono,domicilio,fecha_nacimiento]))
    return apiOperacionesComunes.respJson('yes',"El paciente fue guardado correctamente",{})