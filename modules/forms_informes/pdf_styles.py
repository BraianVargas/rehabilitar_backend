from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.colors import *
from reportlab.platypus import TableStyle



# Configuración del estilo del documento
styles = getSampleStyleSheet()
header_style = styles['Heading1']
title_style = ParagraphStyle(
    'TitleStyle',
    fontSize = 18,
    parent=styles['Heading1'],
    alignment=1,  # 0=left, 1=center, 2=right
    spaceAfter=12,
    spaceBefore=12
)
footer_style = ParagraphStyle(
    'FooterStyle',
    parent=styles['BodyText'],
    alignment=1,
    fontSize=7,
    textColor=colors.grey,  
)
# Crear un estilo para el párrafo que contiene la tabla
style_ddjj = ParagraphStyle(
    'CustomStyle',  # Nombre del estilo
    parent=styles['Normal'],  # Puedes ajustar el estilo base según tus necesidades
    fontSize=10,
    spaceAfter=10,
    spaceBefore=10,
    textColor='black',  # Color del texto
)
icon_span_style = ParagraphStyle(
    'span_style',
    fontSize=10,
    parent=styles['Normal'],
    alignment=1,  # 0=left, 1=center, 2=right
    spaceAfter = 10,
    spaceBefore = 10,
    spaceTop = 10,
    spaceBottom = 10,
)
header_antecedentes_style = ParagraphStyle(
    'antec_styles',
    fontSize=8,
    parent=styles['Heading1'],
    alignment=1,  # 0=left, 1=center, 2=right
    spaceAfter=12,
    spaceBefore=12,
    textColor=white  # Set text color to white
)
table_antecedentes_style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), '#EF6565'),  # Background color for the header row
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Text color for the header row
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Middle align all cells
    ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid lines
    ('SPAN', (0, 0), (-1, 0)),  # Span header across all columns
])
header_consentimiento_style = ParagraphStyle(
    'antec_styles',
    fontSize=12,
    parent=styles['Heading1'],
    alignment=1,  # 0=left, 1=center, 2=right
    spaceAfter=12,
    spaceBefore=12,
    textColor=white  # Set text color to white
)