import datetime
import holidays

def verifica_habil_feriado(fecha):
    # Define el país para el que deseas verificar los feriados y días hábiles
    pais = "AR"  # Puedes cambiar esto al código de tu país

    # Crea un objeto de feriados para el país seleccionado
    feriados = holidays.CountryHoliday(pais)

    # Convierte la fecha en un objeto datetime
    fecha_dt = datetime.datetime.strptime(fecha, "%d/%m/%Y").date()

    # Verifica si la fecha es un feriado o un día hábil
    if fecha_dt in feriados:
        return "feriado"
    else:
        # Si no es feriado, verifica si es un día de la semana laborable (de lunes a viernes)
        if fecha_dt.weekday() < 5:  # 0 es lunes, 4 es viernes
            return "habil"
        else:
            return "fin de semana"

# Ejemplo de uso
fecha = "13/10/2023"
resultado = verifica_habil_feriado(fecha)
print(resultado + " " +fecha)
