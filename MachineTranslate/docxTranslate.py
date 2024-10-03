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
            # original_text = ''.join([t.text for t in text_elements if t.text])
            # if original_text.strip():
            #     # Translate the entire paragraph text once
            #     translated_text = textTranslate.translate_text(original_text, source_lang, target_lang)

            #     # Split the translated text to match the number of original text elements
            #     translated_parts = translated_text.split()  # This may need a more sophisticated split
            #     print("translated_parts", translated_parts)
            #     for i, t in enumerate(text_elements):
            #         if i < len(translated_parts):
            #             t.text = translated_parts[i]
            #         else:
            #             t.text = ''
            for t in text_elements:
                if t.text:
                    t.text = textTranslate.translate_text(t.text, source_lang, target_lang)

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
