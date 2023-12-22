from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image, Table
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import TableStyle

import os
import string, secrets
from config import *
import datetime
import apiDB
from datetime import datetime

from .pdf_styles import *

ALLOWED_IMAGE_EXTENSIONS=['png','jpg','jpeg','jfif']


def fileNameGen():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20))
    return password

def get_tipo_ficha_name(id_ficha):
    query = "SELECT nombre_ficha from tipo_ficha where id = '%s'"
    return apiDB.consultaSelect(query, (id_ficha,))[0]['nombre_ficha']

def genera_cabecera(title):
    # logo_path = "static/img/main-logo.png"
    pass


def genera_ddjj(info_turno ,info_paciente, ddjj_paciente):
    logo_path = "static/img/main-logo.png"
    file_path = f"./files/temp/informe.pdf"     
    # Contenido del PDF
    content = []   

    # Crear el documento PDF
    pdf = SimpleDocTemplate(file_path, pagesize=letter, leftMargin=20, rightMargin=20, topMargin=20, bottomMargin=20)
    
    # Header con imagen (logo de la empresa)
    logo = Image(logo_path, width=120, height=50)
    logo.hAlign = 'LEFT'

    # Título centrado en la misma fila que el logo
    title_text = "<h1 style='font-size: 40px;'><b>Declaración Jurada</b></h1>"
    title = Table([[logo, Spacer(1, 1), Paragraph(title_text)]], colWidths=[2*inch, 1*inch, 5*inch])
    title.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))

    # Generar datos de la tabla
    fecha_nacimiento = info_paciente['fecha_nacimiento']
    fecha_actual = datetime.now()
    edad = fecha_actual.year - fecha_nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

    data = f"""
        <b>Nombre y Apellido:</b> {info_paciente['nombres']} {info_paciente['apellidos']}
        <br/>
        <b>Edad:</b> &nbsp;&nbsp; {edad}  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <b>Documento:</b> &nbsp;&nbsp; {info_paciente['documento']}  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <b>Fecha:</b> &nbsp;&nbsp; {fecha_actual.date()}  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <br/>
        <b>Tipo de Ficha:</b> {get_tipo_ficha_name(info_turno['tipo_ficha_id'])} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
        <br/>
        <b>Tipo de Examen:</b> {(info_turno['tipo_examen']).upper()} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    """
    fecha = info_turno['fecha']
    fecha=str(fecha.year) + "/"+ str(fecha.month)+ "/"+ str(fecha.day )
    name_photo = info_turno['img_token']
    foto_path="files/imagenes/FOTO/"+fecha+'/'+info_paciente['documento']+'/'

    if name_photo != None:        
        for ext in ALLOWED_IMAGE_EXTENSIONS:
            path_aux = foto_path + name_photo + '.' + ext
            if os.path.exists(path_aux):
                foto_path = path_aux
    else:
        foto_path = 'static/img/photo_not_found.jpg'
    foto =  Image(foto_path, width=60,height=60)
    header = Table([[Paragraph(data), Spacer(1, 0), foto]], colWidths=[5*inch, .5*inch, 1*inch])
    header.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'LEFT')]))

    # Crear la tabla
    table = Paragraph(data)

    # Footer con texto
    footer_text = "<br/> 9 de Julio 433 Oeste - (5400) Capital - San Juan - Tels.: 0264-4202469 ó 0264-4225546 - Email: rehabilitasj@speedy.com.ar <br/> <b>Rehabilitar San Juan 2023 © Todos los derechos reservados </b> "
    footer = Paragraph(footer_text, footer_style)

    # Agregar elementos al contenido del PDF
    content.append(title)
    content.append(Spacer(1, 12))
    content.append(header)
    content.append(Spacer(1, 12))
    content.append(footer)

    # Construir el PDF
    pdf.build(content)