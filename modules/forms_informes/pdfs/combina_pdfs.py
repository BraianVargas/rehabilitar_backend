import PyPDF2
import os

def combinar_pdfs(input_folder, output_file):
    pdf_writer = PyPDF2.PdfWriter()

    # Obtener la lista de archivos PDF en la carpeta de entrada
    pdf_files = [f for f in os.listdir(input_folder) if f.endswith('.pdf')]

    # Ordenar los archivos por nombre para mantener un orden específico
    pdf_files.sort()

    # Recorrer cada archivo PDF y agregar sus páginas al escritor
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_folder, pdf_file)
        pdf_reader = PyPDF2.PdfReader(pdf_path)

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)

    # Crear el directorio si no existe
    output_directory = os.path.dirname(output_file)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Guardar el archivo PDF combinado
    with open(output_file, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

# Ejemplo de uso
# input_folder = "files/informes/temp"  # Reemplaza con la ruta real de tus archivos PDF
# output_file = "files/informes/temp/comb/combined.pdf"  # Ruta para el PDF combinado

# combinar_pdfs(input_folder, output_file)
