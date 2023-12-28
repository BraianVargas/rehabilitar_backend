from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, HRFlowable, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.units import cm, inch
from reportlab.platypus import TableStyle

import os
import string, secrets
from config import *
import datetime
import apiDB
from datetime import datetime
import locale

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
        ('ALIGN', (1, 0), (1, 0), 'LEFT')
    ]))
    line = HRFlowable(width="100%", thickness=1, spaceAfter=5, color="black")
    return title,line

def get_personal_data(info_paciente, info_turno, fecha):
    
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
    name_photo = info_turno['img_token']
    foto_path = get_foto_paciente(fecha, name_photo, info_paciente['documento'], "foto")
    foto =  Image(foto_path, width=60,height=60)
    personal_data = Table([[Paragraph(personal_data_body), Spacer(1, 0), foto]], colWidths=[5*inch, .5*inch, 1*inch])
    personal_data.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'LEFT')]))

    return personal_data


def genera_footer():
    # Footer con texto
    footer_text = "<br/> 9 de Julio 433 Oeste - (5400) Capital - San Juan - Tels.: 0264-4202469 ó 0264-4225546 - Email: rehabilitasj@speedy.com.ar <br/> <b>Rehabilitar San Juan 2023 © Todos los derechos reservados </b> "
    footer = Paragraph(footer_text, footer_style)
    return footer

def get_foto_paciente(fecha,name_photo,documento_paciente,tipo):
    foto_path="files/imagenes/"+tipo.upper()+'/'+fecha+'/'+documento_paciente+'/'
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

    return foto_path

def get_firma_paciente(fecha,name_firma, documento_paciente,tipo):
    firma_path = f"files/imagenes/{str(tipo.upper())}/{str(fecha)}/{str(documento_paciente)}/"
    if os.path.exists(firma_path):
        if name_firma != None:
            for ext in ALLOWED_IMAGE_EXTENSIONS:
                path_aux = f"{firma_path}/{name_firma}.{ext}"
                if os.path.exists(path_aux):
                    firma_path = path_aux
        else:
            firma_path = "static/img/firma_not_found.png"
    else:
        firma_path = "static/img/firma_not_found.png"
    return firma_path


def genera_ddjj(info_turno ,info_paciente, ddjj_paciente):

    file_path = f"files/informes/temp/"

    if not os.path.exists(file_path):
        os.makedirs(file_path)
    # Contenido del PDF
    content = []
    header, linea = genera_cabecera(title_text = "<b>Declaración Jurada</b>")
    content.append(header)
    content.append(linea)

    # Crear el documento PDF
    file_path = file_path + info_paciente['documento'] + '- ddjj'+ '.pdf'
    pdf = SimpleDocTemplate(file_path, pagesize=letter, leftMargin=20, rightMargin=20, topMargin=20, bottomMargin=20)

    # Generar datos de la tabla
    fecha = info_turno['fecha']
    fecha=str(fecha.year) + "/"+ str(fecha.month)+ "/"+ str(fecha.day )
    
    personal_data = get_personal_data(info_paciente, info_turno, fecha)


    yes_icon="<span color='green'>&#10004;</span>"
    no_icon="<span color='red'>&#10006;</span>"
    data_antecendentes = [
            [Paragraph('<h3>Antecedentes</h3>',header_antecedentes_style)],
            [
                Paragraph("¿Sufrió algún accidente de tránsito?"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['accidente_transito'] == 1 else Paragraph(no_icon, style=icon_span_style)
            ],
            [
                Paragraph("¿Fuma o ha fumado con anterioridad?"), Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['fuma'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("¿Cuántos por día?"), Paragraph(str(ddjj_paciente[0]['d_fuma']), style=icon_span_style),
            ],
            [
                Paragraph("¿Practica algun deporte?"), Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['deporte'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("¿Cuál?"), Paragraph(str(ddjj_paciente[0]['d_deporte']), style=icon_span_style),
            ],
            [
                Paragraph("¿Consume bebidas alcoholicas?"), Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['fuma'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("¿Cuáles?"), Paragraph(str(ddjj_paciente[0]['d_fuma']), style=icon_span_style),
            ],
            [
                Paragraph("¿Duerme bien?"), Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['fuma'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("¿Cuántas horas por día?"), Paragraph(str(ddjj_paciente[0]['d_fuma']), style=icon_span_style),
            ],
    ]
    col_widths = [3* inch, 2*cm] * 5
    antecedentes_table = Table(data_antecendentes, col_widths)
    antecedentes_table.setStyle(table_antecedentes_style)

    data_antecendentes = [
            [Paragraph('<h3>Antecedentes Personales</h3>',header_antecedentes_style)],
            [
                Paragraph("Dificultad en su vision"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['vision'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Cancer"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['cancer'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Operaciones"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['operaciones'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Dificultad en la audicion"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['audio'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Perdida de peso"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['perdida_peso'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Apendicitis"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['apendicitis'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Dolor de cabeza"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['dolor_cabeza'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Diabetes"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['diabetes'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Vesicula"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['vesicula'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Dolor de torax"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['dolor_torax'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Diabetes 2"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['diabetes_2'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Varices"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['varices'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Taquicardia o palpitaciones"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['taquicardia'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Tratamiento psiquiátrico"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['psiquiatrico'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Tumor"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['tumor'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Hipertension"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['hipertension'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Convulsiones, epilepsia"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['epilepsia'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Hernias, eventraciones"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['hernias'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Marcapasos"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['marcapaso'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Dolor de cintura"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['dolor_cintura'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Corazon"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['corazon'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Falta de aire"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['falta_aire'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Dolor de espalda"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['dolor_espalda'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Rodillas"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['rodillas'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Hepatitis"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['hepatitis'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Dolor de piernas al caminar"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['dolor_piernas'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Tobillos"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['tobillos'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Alergias"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['alergia'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Fracturas"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['fracturas'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Hombros"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['hombros'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
    ]

    col_widths = [2.13* inch, 1*cm] * 10
    antecedentes_personales_table = Table(data_antecendentes, col_widths)
    antecedentes_personales_table.setStyle(table_antecedentes_style)
    leyenda = "<b>&nbsp;&nbsp;&nbsp;Declaro que la información suministrada es verídica. </b>"
    
    name_photo = info_turno['firma_token']
    firma_path= get_firma_paciente(fecha, name_photo, info_paciente['documento'], "firma")
    firma = Image(firma_path,width=120,height=60)


    Firma = Table(
        [
            [
                Spacer(15,0),Spacer(15,0),firma
            ],
            [
                Spacer(15,0),Spacer(15,0),linea
            ],
            [
                Spacer(15,0),Spacer(15,0),Paragraph("Firma del paciente")
            ]
        ]
    )
    # Agregar elementos al contenido del PDF
    content.append(personal_data)
    content.append(linea)
    content.append(Spacer(1, 20))
    content.append(antecedentes_table)
    content.append(Spacer(1, 20))
    content.append(antecedentes_personales_table)
    content.append(Spacer(1, 5))
    content.append(Paragraph(leyenda))
    content.append(Spacer(0, 20))
    content.append(Firma)
    content.append(Spacer(1, 50))
    content.append(linea)
    content.append(genera_footer())

    pdf.build(content)


def genera_consentimiento(info_paciente, info_turno):
    file_path = "files/informes/temp/"
    
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    # Contenido del PDF
    content = []
    header, linea = genera_cabecera(title_text = "<b>Consentimiento</b>")
    content.append(header)
    content.append(linea)
    
    # Crear el documento PDF
    file_path = file_path + info_paciente['documento'] + ' - consentimiento' + '.pdf'
    pdf = SimpleDocTemplate(file_path, pagesize=letter, leftMargin=20, rightMargin=20, topMargin=20, bottomMargin=20)
    fecha = info_turno['fecha']
    fecha=str(fecha.year) + "/"+ str(fecha.month)+ "/"+ str(fecha.day )

    # Generar datos de la tabla
    name_photo = info_turno['img_token']
    


    head_concentimiento = [
            [Paragraph('<h3>CONSENTIMIENTO INFORMADO PARA EXAMENES DE LABORATORIO</h3>',header_consentimiento_style)],
    ]

    col_widths = [7.5* inch] * 1
    head_concentimiento_table = Table(head_concentimiento, col_widths)
    head_concentimiento_table.setStyle(table_antecedentes_style)
    
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8') 

    body_consentimiento = f"""
    Por la presente autorizo a la empresa Rehabilitar San Juan S.R.L se me efectúen 
    los siguientes analisis declarando que se me explicó cada uno de ellos y doy mi concentimiento libremente. <br/><br/>
    Acepto se me realicen pruebas en orina para dosaje de sustancias de adicción: Marihuana y Cocaina.
    <br/> <br/> <br/> <br/> 

    <b>APELLIDO Y NOMBRE: </b> {info_paciente['apellidos']}, {info_paciente['nombres']} <br/> <br/> 
    <b>N° de documento: </b> {info_paciente['documento']} <br/> <br/> 
    <b>Fecha de nacimiento: </b> {info_paciente['fecha_nacimiento'].strftime("%d/%m/%Y")} <br/> <br/> 
    <b>Lugar y fecha: </b> San Juan, {datetime.now().strftime("%d de %B de %Y")} <br/> <br/> 
    
    """

    name_photo = info_turno['firma_token']
    firma_path= get_firma_paciente(fecha, name_photo, info_paciente['documento'], "firma")
    firma = Image(firma_path,width=120,height=60)


    Firma = Table(
        [
            [
                firma,
                Spacer(10,0),
                Paragraph(f"{info_paciente['apellidos']}, {info_paciente['nombres']}")
            ],
            [
                linea,
                Spacer(10,0),
                linea
            ],
            [
                Paragraph("Firma del postulante"),
                Spacer(10,0),
                Paragraph("Aclaración")
            ]
        ]
    )


    # Agregar elementos al contenido del PDF
    content.append(get_personal_data(info_paciente, info_turno, fecha))
    content.append(linea)
    content.append(head_concentimiento_table)
    content.append(Spacer(1, 20))
    content.append(Paragraph(body_consentimiento.upper()))
    content.append(Spacer(1, 45))
    content.append(Firma)
    content.append(Spacer(1, 170))
    content.append(linea)
    content.append(genera_footer())

    pdf.build(content)

def genera_clinico(info_campos, info_paciente, info_turno):
    file_path = "files/informes/temp/"

    if not os.path.exists(file_path):
        os.makedirs(file_path)
    # Contenido del PDF
    content = []
    header, linea = genera_cabecera(title_text = "<b>Examen Clínico</b>")

    content.append(header)
    content.append(linea)
    
    # Crear el documento PDF
    file_path = file_path + info_paciente['documento'] + ' - clinico' + '.pdf'
    pdf = SimpleDocTemplate(file_path, pagesize=letter, leftMargin=20, rightMargin=20, topMargin=20, bottomMargin=20)
    fecha = info_turno['fecha']
    fecha = str(fecha.year) + "/"+ str(fecha.month)+ "/"+ str(fecha.day )

    # Generar datos de la tabla
    name_photo = info_turno['img_token']
    print(info_campos)
    input()
    data_clinico = [
            [Paragraph('<h3>CONSENTIMIENTO INFORMADO PARA EXAMENES DE LABORATORIO</h3>',header_consentimiento_style)],
            [Paragraph("Enfermedades y operaciónes previas:"), Paragraph("{}") ]
    ]

    col_widths = [3.5* inch, 2 *inch] * 1
    data_clinico_table = Table(data_clinico, col_widths)
    data_clinico_table.setStyle(table_antecedentes_style)
    
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8') 


    name_photo = info_turno['firma_token']
    firma_path= get_firma_paciente(fecha, name_photo, info_paciente['documento'], "firma")
    firma = Image(firma_path,width=120,height=60)


    Firma = Table(
        [
            [
                firma,
                Spacer(10,0),
                Paragraph(f"{info_paciente['apellidos']}, {info_paciente['nombres']}")
            ],
            [
                linea,
                Spacer(10,0),
                linea
            ],
            [
                Paragraph("Firma del postulante"),
                Spacer(10,0),
                Paragraph("Aclaración")
            ]
        ]
    )


    # Agregar elementos al contenido del PDF
    content.append(get_personal_data(info_paciente, info_turno, fecha))
    content.append(linea)
    content.append(head_concentimiento_table)
    content.append(Spacer(1, 20))
    content.append(Paragraph(body_consentimiento.upper()))
    content.append(Spacer(1, 45))
    content.append(Firma)
    content.append(Spacer(1, 170))
    content.append(linea)
    content.append(genera_footer())

    pdf.build(content)