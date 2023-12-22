from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, HRFlowable, Spacer, Image
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

def genera_cabecera(title_text):
    logo_path = "static/img/main-logo.png"

    logo = Image(logo_path, width=120, height=50)
    title = Table(
        [
            [
                logo,
                Paragraph(title_text, title_style),
            ]
        ],
        colWidths=[2*inch, 5*inch]
    )
    title.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER')
    ]))
    line = HRFlowable(width="100%", thickness=1, spaceAfter=5, color="black")
    return title,line

def genera_footer():
    # Footer con texto
    footer_text = "<br/> 9 de Julio 433 Oeste - (5400) Capital - San Juan - Tels.: 0264-4202469 ó 0264-4225546 - Email: rehabilitasj@speedy.com.ar <br/> <b>Rehabilitar San Juan 2023 © Todos los derechos reservados </b> "
    footer = Paragraph(footer_text, footer_style)
    return footer


def genera_ddjj(info_turno ,info_paciente, ddjj_paciente):
    file_path = f"./files/informes/temp/"
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    # Contenido del PDF
    content = []
    header, linea = genera_cabecera(title_text = "<b>Declaración Jurada</b>")
    content.append(linea)
    content.append(header)
    content.append(linea)

    # Crear el documento PDF
    file_path = file_path + info_paciente['documento'] + '.pdf'
    pdf = SimpleDocTemplate(file_path, pagesize=letter, leftMargin=20, rightMargin=20, topMargin=20, bottomMargin=20)


    # Generar datos de la tabla
    fecha_nacimiento = info_paciente['fecha_nacimiento']
    fecha_actual = datetime.now()
    edad = fecha_actual.year - fecha_nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

    personal_data_body = f"""
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
    if os.path.exists(foto_path):
        if name_photo != None:        
            for ext in ALLOWED_IMAGE_EXTENSIONS:
                path_aux = foto_path + name_photo + '.' + ext
                if os.path.exists(path_aux):
                    foto_path = path_aux
        else:
            foto_path = 'static/img/photo_not_found.jpg'
    else:
        foto_path = 'static/img/photo_not_found.jpg'

    foto =  Image(foto_path, width=60,height=60)
    personal_data = Table([[Paragraph(personal_data_body), Spacer(1, 0), foto]], colWidths=[5*inch, .5*inch, 1*inch])
    personal_data.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'LEFT')]))

    print(ddjj_paciente)
    
    data = """
        Antecedentes

    
    """


    # Agregar elementos al contenido del PDF
    content.append(personal_data)
    content.append(Spacer(1, 12))
    content.append(Paragraph(data))
    content.append(linea)
    content.append(genera_footer())

    # Construir el PDF
    pdf.build(content)