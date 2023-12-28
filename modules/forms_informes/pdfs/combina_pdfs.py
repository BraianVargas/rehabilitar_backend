import PyPDF2
import os

def combinar_pdfs(input_folder, output_file):
    pdf_writer = PyPDF2.PdfFileWriter()

    # Obtener la lista de archivos PDF en la carpeta de entrada
    pdf_files = [f for f in os.listdir(input_folder) if f.endswith('.pdf')]

    # Ordenar los archivos por nombre para mantener un orden específico
    pdf_files.sort()

    # Recorrer cada archivo PDF y agregar sus páginas al escritor
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_folder, pdf_file)
        pdf_reader = PyPDF2.PdfFileReader(pdf_path)

        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            pdf_writer.addPage(page)

    # Guardar el archivo PDF combinado
    with open(output_file, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

# Ejemplo de uso
input_folder = "./ruta/de/tus/pdf"  # Reemplaza con la ruta real de tus archivos PDF
output_file = "./ruta/del/archivo/combinado.pdf"  # Ruta para el PDF combinado

combinar_pdfs(input_folder, output_file)
