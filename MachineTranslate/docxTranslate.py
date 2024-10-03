# from docx import Document
# from . import textTranslate
# import os

# def read_docx(path, source_lang, target_lang):
#     if os.path.exists(path):
#         doc = Document(path)

#         translate_paragraphs(doc.paragraphs, source_lang, target_lang)
#         # Translate text in tables
#         translate_tables(doc.tables, source_lang, target_lang)
#         # Translate text in headers and footers
#         for section in doc.sections:
#             translate_headers_footers(section, source_lang, target_lang)
#         # Translate text in footnotes and endnotes if any
#         if hasattr(doc, 'footnotes'):
#             translate_paragraphs(doc.footnotes.paragraphs, source_lang, target_lang)
#         if hasattr(doc, 'endnotes'):
#             translate_paragraphs(doc.endnotes.paragraphs, source_lang, target_lang)

#         save_path = "translated_docx.docx"
#         doc.save(save_path)
#         return save_path

# def translate_paragraphs(paragraphs, source_lang, target_lang):
#     for para in paragraphs:
#         translated_text = textTranslate.translate_text(para.text, source_lang, target_lang)
#         para.text = translated_text  # Replace original text with translated text

# def translate_tables(tables, source_lang, target_lang):
#     for table in tables:
#         for row in table.rows:
#             for cell in row.cells:
#                 translate_paragraphs(cell.paragraphs, source_lang, target_lang)

# def translate_headers_footers(section, source_lang, target_lang):
#     # Translate paragraphs in the header
#     for header_para in section.header.paragraphs:
#         translated_text = textTranslate.translate_text(header_para.text, source_lang, target_lang)
#         header_para.text = translated_text
    
#     # Translate paragraphs in the footer
#     for footer_para in section.footer.paragraphs:
#         translated_text = textTranslate.translate_text(footer_para.text, source_lang, target_lang)
#         footer_para.text = translated_text

# def translate_docx(path, source_lang, target_lang):
#     translated_file_path = read_docx(path, source_lang, target_lang)
#     return translated_file_path
    # return content





import zipfile
from lxml import etree
import os
import shutil
from . import textTranslate

# Function to translate text (replace this with your actual translation function)

def translate_docx(path, source_lang, target_lang):

    # Open the .docx file as a zip
    docx_filename = path
    with zipfile.ZipFile(docx_filename, 'r') as docx:
        # Extract the document.xml file that contains the text
        xml_content = docx.read('word/document.xml')

    # Parse the XML
    tree = etree.fromstring(xml_content)

    # Define namespaces for Word XML
    namespaces = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    }

    # Extract all paragraphs
    paragraphs = tree.xpath('//w:p', namespaces=namespaces)

    # Translate the paragraphs
    for para in paragraphs:
        # Extract text from the paragraph
        text_elements = para.xpath('.//w:t', namespaces=namespaces)
        if text_elements:
            original_text = ''.join([t.text for t in text_elements if t.text])
            if original_text.strip():
                # Translate the entire paragraph text once
                translated_text = textTranslate.translate_text(original_text, source_lang, target_lang)

                # Split the translated text to match the number of original text elements
                translated_parts = translated_text.split()  # This may need a more sophisticated split
                for i, t in enumerate(text_elements):
                    if i < len(translated_parts):
                        t.text = translated_parts[i]
                    else:
                        t.text = ''

    # Save the modified XML
    translated_docx_filename = 'trans.docx'
    output_dir = 'translated_docx_content'
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    # Extract original .docx to a folder
    with zipfile.ZipFile(docx_filename, 'r') as docx:
        docx.extractall(output_dir)

    # Write the modified document.xml to the extracted folder
    with open(os.path.join(output_dir, 'word/document.xml'), 'wb') as f:
        f.write(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='UTF-8'))

    # Create a new .docx file with the modified content
    with zipfile.ZipFile(translated_docx_filename, 'w') as new_docx:
        for foldername, subfolders, filenames in os.walk(output_dir):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path, output_dir)
                new_docx.write(file_path, arcname)

    # Cleanup the temporary folder
    shutil.rmtree(output_dir)

    print(f"Translated document saved as {translated_docx_filename}")
    return translated_docx_filename
