from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image, Table
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, getSampleStyleSheet
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.units import inch
import os
import string, secrets
from config.config import *


###################################################################################
#              GENERA UN TOKEN UNICO PARA EL USUARIO QUE HACE LOGIN
###################################################################################
def fileNameGen():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20))
    return password

def genera_comprobante_turno(nombre, dni, fecha_turno, tipo):
    # Nombre del archivo de salida PDF
    fecha_turno = fecha_turno.replace("/", "-") 
    tipo = tipo.lower()
    
    
    # Ruta completa al directorio donde deseas guardar el PDF
    destino = f"./turnos/{tipo}/{fecha_turno}/"  # Reemplaza esto con la ruta deseada

    if not os.path.exists(destino):
        os.makedirs(destino)

    # Genera token y regenera en caso de existir
    fileToken = fileNameGen()
    while (os.path.exists(destino + fileToken + ".pdf")):
        fileToken = fileNameGen()

    output_file = os.path.join(destino, f"{fileToken}.pdf")
    # Ruta de la imagen de marca de agua
    marca_de_agua = "static/img/main-logo.png"
    #Tamaño de pagina del PDF 
    pdf_width = 500
    pdf_height = 250
    # Tamaño deseado para la marca de agua
    marca_de_agua_width = 400  # Ancho
    marca_de_agua_height = 200  # Alto

    # Crear el objeto PDF con el tamaño personalizado
    pdf = SimpleDocTemplate(output_file, pagesize=(pdf_width, pdf_height))

    # Definir estilo para el texto
    styles = getSampleStyleSheet()
    tipo_style = ParagraphStyle(name='TipoStyle', parent=styles['Normal'], alignment=1, fontName='Times-Roman', fontSize=20, bottomIndent=5)
    nombre_style = ParagraphStyle(name='NombreStyle', parent=styles['Normal'], alignment=1, fontName='Helvetica-Bold', fontSize=12, bottomIndent=5)
    fecha_turno_style = ParagraphStyle(name='FechaTurnoStyle', parent=styles['Normal'], alignment=1, fontName='Helvetica-Bold', fontSize=12, bottomIndent=5)
    dni_style = ParagraphStyle(name='DNIStyle', parent=styles['Normal'], fontName='Helvetica-Bold', alignment=1, fontSize=12, bottomIndent=5)
    enlace_style = ParagraphStyle(name='EnlaceStyle', parent=styles['Normal'], alignment=1, fontName='Courier-Bold',textColor=colors.blue, fontSize=10)

    # Definir plantilla de página con marca de agua
    def add_watermark(canvas, doc):
        canvas.saveState()

        # Dibujar la imagen de marca de agua con opacidad al 10% como fondo
        canvas.setFillColorRGB(1, 1, 1, 0.1)
        # Obtener el tamaño de la página
        page_width = pdf_width
        page_height = pdf_height
        # Calcular la posición centrada de la marca de agua
        x = (page_width - marca_de_agua_width) / 2
        y = (page_height - marca_de_agua_height) / 2

        # Dibujar la imagen de marca de agua en el centro con padding
        canvas.drawImage(marca_de_agua, x, y, width=marca_de_agua_width, height=marca_de_agua_height, mask='auto')

        canvas.restoreState()

    page_template = PageTemplate(id='withwatermark', frames=[Frame(0, 0, pdf_width, pdf_height, id='normal')], onPage=add_watermark)

    pdf.addPageTemplates([page_template])

    # Crear el contenido del PDF
    content = []

    # Agregar contenido con el formato deseado
    enlace = f'<a href="{ROOT_PATH}/ddjj/{dni}"> Enlace a Declaración Jurada</a>'

    tipo_paragraph = Paragraph(tipo.upper(),tipo_style)
    nombre_paragraph = Paragraph("<u>Nombre y Apellido:</u> <br/><br/>" + nombre, nombre_style)
    dni_paragraph = Paragraph("<u>DNI:</u> <br/><br/>" + dni, dni_style)
    fecha_turno_paragraph = Paragraph("<u>Fecha de turno:</u> <br/><br/>" + fecha_turno, fecha_turno_style)
    enlace_paragraph = Paragraph(enlace, enlace_style)

    content.append(Spacer(1, 15))
    content.append(tipo_paragraph)
    content.append(Spacer(1, 20))
    content.append(nombre_paragraph)
    content.append(Spacer(1, 10)) 
    content.append(dni_paragraph)
    content.append(Spacer(1, 10))
    content.append(fecha_turno_paragraph)
    content.append(Spacer(1, 10))
    content.append(enlace_paragraph)

    # Guardar el contenido en el PDF
    pdf.build(content)
    return fileToken

