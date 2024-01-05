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


# --------------------------------------------------------------
# 
#                 Genera Footer
# 
# --------------------------------------------------------------
def genera_footer():
    # Footer con texto
    footer_text = "9 de Julio 433 Oeste - (5400) Capital - San Juan - Tels.: 0264-4202469 ó 0264-4225546 - Email: rehabilitasj@speedy.com.ar <br/> <b>Rehabilitar San Juan 2023 © Todos los derechos reservados </b> "
    footer = Paragraph(footer_text, footer_style)
    return footer

# --------------------------------------------------------------
# 
#                 Genera Foto Paciente
# 
# --------------------------------------------------------------
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

# --------------------------------------------------------------
# 
#                 Genera Firma paciente
# 
# --------------------------------------------------------------

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


# --------------------------------------------------------------
# 
#                 Genera DDJJ
# 
# --------------------------------------------------------------

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
    file_path = file_path + '1'+ '.pdf'
    pdf = SimpleDocTemplate(file_path, pagesize=letter, leftMargin=20, rightMargin=20, topMargin=20, bottomMargin=20)

    # Generar datos de la tabla
    fecha = info_turno['fecha']
    fecha=str(fecha.year) + "/"+ str(fecha.month)+ "/"+ str(fecha.day )
    
    personal_data = get_personal_data(info_paciente, info_turno, fecha)


    yes_icon="<span color='green'>&#10004;</span>"
    no_icon="<span color='red'>&#10006;</span>"
    data_antecendentes = [
            [Paragraph('<h3>Antecedentes Personales</h3>',header_antecedentes_style)],
            [
                Paragraph("Acidéz o trastornos intestinales"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['acidez'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Alergia a drogas o medicamentos"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['alergia_medicamentos'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Articulaciones dolorosas"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['dolor_articulaciones'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Asma"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['asma'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Azucar en sangre (diabetes)"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['azucar'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Brucelosis o fiebre de malta"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['brucelosis'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Cancer u otro tumor"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['cancer_tumor'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Confunde los colores"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['colores'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Convulciones"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['convulcion'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Depresión o preocupación excesiva"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['depresion'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Dificltad en la visión"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['vision'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Dificultad para orinar"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['dificultad_orinar'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Dolor de espalda o cintura"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['dolor_espalda'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Dolor en el hjombro"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['dolor_hombro'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Dolores de cabeza frecuentes"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['dolor_cabeza'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Dolores en el pecho (precordialgia)"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['dolor_pecho'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Dolores en los pies o pie plano"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['dolor_pies'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Dolores en rodillas"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['dolor_rodilla'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Enfermedad de chagas"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['chagas'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Enfermedades de la piel"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['enfermedad_piel'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Enfermedades por contacto sexual"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['enfermedad_sexual'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Falta de aire (disnea)"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['falta_aire'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Familiares con tuberculosis"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['familiares_tuberculosis'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Fracturas o luxaciones"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['fracturas'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Ha sido enyesado alguna vez"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['enyesado'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Ha sido operado alguna vez"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['operado'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Hemorroides"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['hemorroides'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Hernias"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['hernias'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Ictericia (derrame bilial)"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['ictericia'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Indegestión frecuente"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['indigestion'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Insomnio"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['insomnio'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Intoleracia a alguna comida"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['intolerancia_comida'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Mareos o desmayos"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['mareos'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Fuma"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['fuma'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Palpitaciones del corazón"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['palpitaciones'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Perdida de memoria u olvidos frecuentes"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['perdida_memoria'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Perdida de peso reciente"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['perdida_peso'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Pesadillas frecuentes"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['pesadillas'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Presión sanguinea alta"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['presion_alta'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Resfríos frecuentes"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['resfrios'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Sangre en esputo"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['esputo'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Sangre en orina"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['sangre_orina'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Sordera o disminución de la audición"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['sordera'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Sinusitis"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['sinusitis'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Sudores nocturnos"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['sudores_nocturnos'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Supuración de oídos"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['supuracion_oidos'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Trastornos biliares o hepáticos"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['hepaticos'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Ulcera gástrica o duodenal"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['ulcera_gastrica'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Urticaria"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['urticaria'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Várices"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['varices'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Vomitos o acidéz"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['vomitos'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Tiene indemnización pendiente"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['indemnizacion_pendiente'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Menstruaciones Dolorosas"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['dolor_menstruacion'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Flujo"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['flujo'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
            [
                Paragraph("Tuvo que abandonar algún trabajo por razones de salud"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['abandono_por_salud'] == 1 else Paragraph(no_icon, style=icon_span_style),
                Paragraph("Recibió alguna indemnización por accidente de trabajo o enfermedad profesional"), 
                Paragraph(yes_icon, style=icon_span_style) if ddjj_paciente[0]['recibio_indemnizacion'] == 1 else Paragraph(no_icon, style=icon_span_style),
            ],
    ]

    col_widths = [2.13* inch, 1*cm] * 10
    antecedentes_personales_table = Table(data_antecendentes, col_widths)
    antecedentes_personales_table.setStyle(table_antecedentes_style)
    leyenda = "<b>&nbsp;&nbsp;&nbsp;Declaro que la información suministrada es verídica. </b>"
    
    name_photo = info_turno['firma_token']
    firma_path= get_firma_paciente(fecha, name_photo, info_paciente['documento'], "firma")
    firma = Image(firma_path,width=100,height=50)


    Firma = Table(
        [
            [
                Spacer(15,0),Spacer(15,0),firma
            ],
            [
                Spacer(15,0),Spacer(15,0),linea
            ],
            [
                Spacer(20,0),Spacer(20,0),Paragraph("Firma del paciente")
            ]
        ]
    )
    # Agregar elementos al contenido del PDF
    content.append(personal_data)
    content.append(linea)
    content.append(Spacer(1, 5))
    content.append(antecedentes_personales_table)
    content.append(Paragraph(leyenda))
    content.append(Firma)
    content.append(Spacer(1, 5))
    content.append(linea)
    content.append(genera_footer())

    pdf.build(content)


# --------------------------------------------------------------
# 
#                 Genera Consentimiento
# 
# --------------------------------------------------------------

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
    file_path = file_path + '2' + '.pdf'
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

# --------------------------------------------------------------
# 
#                 Genera Exame Clínico SAS
# 
# --------------------------------------------------------------
def genera_sas(info_campos, info_paciente, info_turno):
    file_path = "files/informes/temp/"

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    content = []

    header, linea = genera_cabecera(title_text= f"<b> {str(info_campos[0]['label'])} </b>")

    content.append(header)
    content.append(linea)

    # Crear el documento PDF
    file_path = file_path + '4' + '.pdf'
    pdf = SimpleDocTemplate(file_path, pagesize=letter, leftMargin=20, rightMargin=20, topMargin=20, bottomMargin=20)
    fecha = info_turno['fecha']
    fecha = str(fecha.year) + "/"+ str(fecha.month)+ "/"+ str(fecha.day )

    # Generar datos de la tabla
    name_photo = info_turno['img_token']

    data_clinico = [
        [Paragraph(info_campos[0]["label"], header_consentimiento_style)],
    ]
    i = 3
    while i < len(info_campos):
        data_clinico.append(
            [
                Paragraph(f"{info_campos[i]['label']}"),
                Paragraph(f"{str(info_campos[i]['value'])}"),
                Paragraph(f"{info_campos[i+1]['label']}"),
                Paragraph(f"{str(info_campos[i+1]['value'])}")
            ]
        )
        i = i + 2

    col_widths = [2.5* inch, 1.5 *inch, 2.5 * inch , 1.5*inch] * 30
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
    content.append(data_clinico_table)
    content.append(Spacer(1, 250))
    content.append(Firma)
    content.append(Spacer(1, 250))
    content.append(linea)
    content.append(genera_footer())

    pdf.build(content)
# --------------------------------------------------------------
# 
#                 Genera Examen Clínico
# 
# --------------------------------------------------------------

def genera_clinico(info_campos, info_paciente, info_turno):
    file_path = "files/informes/temp/"

    if not os.path.exists(file_path):
        os.makedirs(file_path)
    # Contenido del PDF
    content = []
    header, linea = genera_cabecera(title_text = f"<b>{info_campos[0]['label']}</b>")

    content.append(header)
    content.append(linea)
    
    # Crear el documento PDF
    file_path = file_path + '3' + '.pdf'
    pdf = SimpleDocTemplate(file_path, pagesize=letter, leftMargin=20, rightMargin=20, topMargin=20, bottomMargin=20)
    fecha = info_turno['fecha']
    fecha = str(fecha.year) + "/"+ str(fecha.month)+ "/"+ str(fecha.day )

    # Generar datos de la tabla
    name_photo = info_turno['img_token']
        
    data_clinico = [
        [Paragraph(info_campos[0]["label"], header_consentimiento_style)],
    ]
    i = 3
    observaciones_agregadas = set() 
    while i < len(info_campos):
        if info_campos[i]['observaciones'] == "general" and info_campos[i]['label'] not in observaciones_agregadas:
            data_clinico.append(
                [
                    Paragraph(f"{info_campos[i]['label']}"),
                    Paragraph(f"{str(info_campos[i]['value'])}"),
                    Paragraph(f"{info_campos[i+1]['label']}"),
                    Paragraph(f"{str(info_campos[i+1]['value'])}")
                ]
            )
            observaciones_agregadas.add(info_campos[i]['label'])

        i = i + 2
    sas_gen = nor_gen = pre_gen = False

    sas = []
    for campo in info_campos:
        observaciones = campo['observaciones']
        if not sas_gen and observaciones!=None and "sas" in observaciones:
            sas.append(campo)
        
        # if not nor_gen and "nordico" in observaciones:
        #     genera_nordico(campo)
        #     nor_gen = True

        # if not pre_gen and "preocupacional" in observaciones:
        #     genera_preocupacional(campo)
        #     pre_gen = True
            

    if len(sas) != 0:
        genera_sas(sas, info_paciente, info_turno)
    
  
    col_widths = [2.5* inch, 1.5 *inch, 2.5 * inch , 1.5*inch] * 30
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
    content.append(data_clinico_table)
    content.append(Spacer(1, 50))
    content.append(Firma)
    content.append(Spacer(1, 100))
    content.append(linea)
    content.append(genera_footer())

    pdf.build(content)