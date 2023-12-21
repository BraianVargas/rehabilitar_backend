from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors



# Configuración del estilo del documento
styles = getSampleStyleSheet()
header_style = styles['Heading1']
title_style = ParagraphStyle(
    'TitleStyle',
    parent=styles['Heading1'],
    alignment=1,  # 0=left, 1=center, 2=right
    spaceAfter=12,
)
footer_style = ParagraphStyle(
    'FooterStyle',
    parent=styles['BodyText'],
    alignment=1,
    fontSize=8,
    textColor=colors.grey,
)

