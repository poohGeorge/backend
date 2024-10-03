from pdf2docx import Converter
from docx2pdf import convert
from . import docxTranslate, textTranslate

def convert_pdf2docx(path):
    pdf_file = path
    docx_file = 'pdf2docx.docx'

    # Create a Converter object
    cv = Converter(pdf_file)
    # Convert the PDF to DOCX
    cv.convert(docx_file, start=0, end=None)
    # Close the Converter
    cv.close()
    return docx_file

def convert_docx2pdf(path):
    # Convert DOCX to PDF
    docx_file = path
    pdf_file = 'docx2pdf.pdf'
    print("docx_file", docx_file)
    # Convert the file
    convert(docx_file, pdf_file)
    return pdf_file

def translate_pdf(file_path, source_lang, target_lang):
    pdf2docx_path = convert_pdf2docx(file_path)
    translated_file_path = docxTranslate.translate_docx(pdf2docx_path, source_lang, target_lang)
    docx2pdf_path = convert_docx2pdf(translated_file_path)
    return docx2pdf_path
